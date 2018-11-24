import pandas as pd
import numpy as np
from collections import Counter
import tqdm
import math
from sklearn.metrics import mean_squared_error
import warnings
# warnings.filterwarnings('ignore')
import random
from random import randint

import tensorflow as tf

from CF.collaborative_filtering import locationRec

recmodel = locationRec()
recmodel.datapipeline(preproccesing=2)

user = recmodel.train.user_nickname.tolist()
items = recmodel.train.town.tolist()
num_items = len(set(items))
num_user = len(set(user))
print("#Items: {}, #user: {}".format(num_items, num_user))


# Network Parameters
epochs = 100
batch_size = 250
num_input = num_items   # num of items
num_hidden_1 = 15       # 1st layer num features
num_hidden_2 = 10 # 2nd layer num features (the latent dim)

weights = {
    'encoder_h1': tf.Variable(tf.random_normal([num_input, num_hidden_1], dtype=tf.float64)),
    'encoder_h2': tf.Variable(tf.random_normal([num_hidden_1, num_hidden_2], dtype=tf.float64)),
    'decoder_h1': tf.Variable(tf.random_normal([num_hidden_2, num_hidden_1], dtype=tf.float64)),
    'decoder_h2': tf.Variable(tf.random_normal([num_hidden_1, num_input], dtype=tf.float64)),
}

biases = {
    'encoder_b1': tf.Variable(tf.random_normal([num_hidden_1], dtype=tf.float64)),
    'encoder_b2': tf.Variable(tf.random_normal([num_hidden_2], dtype=tf.float64)),
    'decoder_b1': tf.Variable(tf.random_normal([num_hidden_1], dtype=tf.float64)),
    'decoder_b2': tf.Variable(tf.random_normal([num_input], dtype=tf.float64)),
}

def encoder(x):
    # Encoder Hidden layer with sigmoid activation #1
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['encoder_h1']), biases['encoder_b1']))
    # Encoder Hidden layer with sigmoid activation #2
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['encoder_h2']), biases['encoder_b2']))
    return layer_2

# Building the decoder

def decoder(x):
    # Decoder Hidden layer with sigmoid activation #1
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['decoder_h1']), biases['decoder_b1']))
    # Decoder Hidden layer with sigmoid activation #2
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['decoder_h2']), biases['decoder_b2']))
    return layer_2


def main():

	X = tf.placeholder(tf.float64, [None, num_input])

	# Construct model
	encoder_op = encoder(X)
	decoder_op = decoder(encoder_op)
	y_pred = decoder_op
	y_true = X

	# Define loss and optimizer, minimize the squared error

	loss = tf.losses.mean_squared_error(y_true, y_pred)
	optimizer = tf.train.RMSPropOptimizer(0.1).minimize(loss)

	predictions = pd.DataFrame()


	matrix = recmodel.user_item_df.values


	# Initialize the variables (i.e. assign their default value)
	saver = tf.train.Saver()
	init = tf.global_variables_initializer()
	local_init = tf.local_variables_initializer()
	save_dir = "./model/cf_tf/"
	i_global=0

	with tf.Session() as session:
	    session.run(init)
	    session.run(local_init)
	    train_writer = tf.summary.FileWriter(save_dir, session.graph)

	    num_batches = int(matrix.shape[0] / batch_size)
	    matrix = np.array_split(matrix, num_batches)

	    for i in range(20):

	        avg_cost = 0

	        for batch in matrix:
	            _, l = session.run([optimizer, loss], feed_dict={X: batch})
	            avg_cost += l

	        avg_cost /= num_batches

	        print("Epoch: {} Loss: {}".format(i + 1, avg_cost))

	        # if i % display_step == 0 or i == 1:
	        #     print('Step %i: Minibatch Loss: %f' % (i, l))
	        
	    summary = tf.Summary(value=[
	            tf.Summary.Value(tag="loss/test", simple_value=avg_cost),])
	        
	    train_writer.add_summary(summary, i_global)

	    saver.save(session, save_path=save_dir, global_step=i_global)

	    print("Predictions...")

	    matrix = train.values
	    
	    preds = session.run(decoder_op, feed_dict={X: matrix})

	    #print(matrix.shape)
	    #print(preds.shape)

	    predictions = predictions.append(pd.DataFrame(preds))

	    predictions = predictions.stack().reset_index(name='checkins')
	    predictions.columns = ['user_nickname', 'town', 'checkins']
	    predictions['user_nickname'] = predictions['user_nickname'].map(lambda value: user_nicknames[value])
	    predictions['town'] = predictions['town'].map(lambda value: items[value])

	    #print(predictions.shape)

	    print("Filtering out items in training set")

	    keys = ['user_nickname', 'town']
	    i1 = predictions.set_index(keys).index
	    i2 = recmodel.validate.set_index(keys).index

	    recs = predictions[~i1.isin(i2)]
	    recs = recs.sort_values(['user_nickname', 'checkins'], ascending=[True, False])
	    recs = recs.groupby('user_nickname').head(k)
	    recs.to_csv('recs.tsv', sep='\t', index=False, header=False)
	    
	    #recs

	#     test = pd.read_csv(test_data, sep='\t', names=['user_nickname', 'item', 'checkins', 'timestamp'], header=None)
	#     test = test.drop('timestamp', axis=1)
	    test = recmodel.test
	    test = test.sort_values(['user_nickname', 'checkins'], ascending=[True, False])

	    #test = test.groupby('user_nickname').head(k) #.reset_index(drop=True)
	    #test_list = test.as_matrix(columns=['town']).reshape((-1))
	    #recs_list = recs.groupby('user_nickname').head(k).as_matrix(columns=['town']).reshape((-1))

	    print("Evaluating...")

	    p = 0.0
	    for user in users[:10]:
	        test_list = test[(test.user_nickname == user)].head(k).as_matrix(columns=['town']).flatten()
	        recs_list = recs[(recs.user_nickname == user)].head(k).as_matrix(columns=['town']).flatten()

	        #session.run(pre_op, feed_dict={eval_x: test_list, eval_y: recs_list})

	        pu = precision_score(test_list, recs_list, average='micro')
	        p += pu

	        print("Precision for user {}: {}".format(user, pu))
	        print("user test:--\n{}".format([mov_dict[x][1] for x in test_list]))
	        print("user recs:--\n{}".format([mov_dict[x][1] for x in recs_list]))
	        print()
	    p /= 10#len(user_nicknames)

	    #p = session.run(pre)
	    print("Precision@{}: {}".format(k, p))


if __name__ == '__main__':
	main()