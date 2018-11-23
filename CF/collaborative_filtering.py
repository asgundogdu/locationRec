#!/usr/bin/python

#####################
#### Imports
#####################

import pandas as pd
import numpy as np
from collections import Counter
import tqdm
import math
from sklearn.metrics import mean_squared_error
from scipy.sparse.csgraph import minimum_spanning_tree as mst_nsim
from scipy.sparse.linalg import svds

# For visualization


# Created modules
def compute_rmse(preds, ground_truth):
    grouped = pd.DataFrame({'count' : ground_truth.groupby(['user_nickname','town'])['town'].apply(len)}).reset_index()
    pred_values = []
    real_values = []
     
    for index, row in tqdm.tqdm(grouped.iterrows(), total=grouped.shape[0], position=0):
        user_index = preds.index.tolist().index(row['user_nickname'])
        town_index = preds.columns.tolist().index(row['town'])
        #pred_values.append(predictions[(predictions.index==row['user_nickname'])][row['town']][0])
        pred_values.append(preds.iloc[user_index,town_index])
        real_values.append(float(row['count']))
    rms = math.sqrt(mean_squared_error(real_values, pred_values))
    return rms


def compute_precision_recall_N(PR, valid, N):

    grouped_val = pd.DataFrame({'count' : valid.groupby(['user_nickname','town'])['town'].apply(len)}).reset_index()

    concat_preds = pd.DataFrame()
    for interval in range(1000,PR.shape[0]+1000,1000):
        flat_preds = pd.melt(PR.iloc[interval-1000:interval], 
                        id_vars='user_nickname', 
                        value_vars=PR.iloc[interval-1000:interval].columns, # list of days of the week
                        var_name='town', 
                        value_name='predicted_count')
        flat_preds['user_nickname'] = PR.iloc[interval-1000:interval].index.tolist() * len(PR.columns)
        flat_preds = flat_preds[flat_preds.predicted_count >= 0.]

        flat_preds = flat_preds.groupby('user_nickname')[['user_nickname','town','predicted_count']].apply(lambda grp: grp.nlargest(N,'predicted_count'))

        concat_preds = pd.concat([concat_preds, flat_preds], axis=0)

    tp, fp, fn = 0.,0.,0.

    for user in tqdm.tqdm(grouped_val.user_nickname.unique().tolist(), total=len(grouped_val.user_nickname.unique().tolist()), position=0):
        tmp_val_df = grouped_val[grouped_val.user_nickname==user] 

        if tmp_val_df.shape[0] != 0:    
            tmp_pr_towns = concat_preds[concat_preds.user_nickname==user].town.tolist()
            tmp_val_towns = tmp_val_df.town.tolist()


            for gt_town in tmp_val_towns:
                if gt_town in tmp_pr_towns:
                    #print('TP')
                    tp+=1.
                elif gt_town not in tmp_pr_towns:
                    #print('FN')
                    fn+=1.

            for pr_town in tmp_pr_towns[:len(tmp_val_towns)]:
                if pr_town not in tmp_val_towns:
                    fp+=1.
                    #print('FP')  
    return tp,fp,fn


def svd_model(user_item_df, latent_dimension):
    Checkins_demeaned = user_item_df.values/np.mean(user_item_df.values)
    U, sigma, Vt = svds(Checkins_demeaned, latent_dimension)
    sigma = np.diag(sigma)
    all_user_predicted_checkins = np.dot(np.dot(U, sigma), Vt) + np.mean(user_item_df.values)
    preds = pd.DataFrame(all_user_predicted_checkins, columns = user_item_df.columns, index=user_item_df.index)
    return preds

#####################
#### Class
#####################

class locationRec(object):
    """DocString"""
    def __init__(self):
        self.user_item_df = None
        self.train = None
        self.validate = None
        self.test = None
        self.preds = None

        self.rmse_train = None
        self.rmse_val = None
        self.rmse_test = None

        self.precision_train = None
        self.recall_train = None
        self.precision_val = None
        self.recall_val = None
        self.precision_test = None
        self.recall_test = None

        self.model = None


    def datapipeline(self, preproccesing=1):
        if preproccesing==1:
            self.user_item_df = pd.read_pickle('User_Item.pckl')
            self.train = pd.read_pickle('train.pckl')
            self.validate = pd.read_pickle('validate.pckl')
            self.test = pd.read_pickle('test.pckl')


    def train_model(self, model_type='SVD', latent_dimension=50):
        if model_type == 'SVD':
            print('Training using SVD model...')
            self.preds = svd_model(self.user_item_df, latent_dimension)
        elif model_type == 'SVD++':
            pass
        elif model_type == 'AutoEncoder':
            pass
        print('Done')


    def eval_rmse(self, data='val'):
        if data == 'val':
            self.rmse_val = compute_rmse(self.preds, self.validate)
        elif data == 'train':
            self.rmse_val = compute_rmse(self.preds, self.train)
        elif data == 'test':
            self.rmse_val = compute_rmse(self.preds, self.test)


    def eval_precision_N(self, N, data = 'val'):
        #compute_precision_recall_N(PR, valid, N)
        if data == 'val':
            tp,fp,fn = compute_precision_recall_N(self.preds, self.validate, N)
            self.precision_val = tp/(tp+fp)
            self.recall_val = tp/(tp+fn)
        elif data == 'train':
            tp,fp,fn = compute_precision_recall_N(self.preds, self.train, N)
            self.precision_train = tp/(tp+fp)
            self.recall_train = tp/(tp+fn)
        elif data == 'test':
            tp,fp,fn = compute_precision_recall_N(self.preds, self.test, N)
            self.precision_test = tp/(tp+fp)
            self.recall_test = tp/(tp+fn)
        else:
            print("'data' should be equal to 'val', 'train', or 'test'!!!")

        return (tp/(tp+fp), tp/(tp+fn))


    def recommend_N_cities_for_user(self, N, user, data='val'):
        # Get User Index
        user_index = self.preds.index.tolist().index(user)
        # Get Sorted User recommendations
        recommended_list_sorted = self.preds.iloc[user_index,:].sort_values(ascending=False).head(N).index.tolist()

        if data=='val':
            val_user_df = self.validate[self.validate.user_nickname == user]
            actual_list = val_user_df.user_nickname.tolist()
        if data=='test':
            val_user_df = self.test[self.test.user_nickname == user]
            actual_list = val_user_df.user_nickname.tolist()

        return recommended_list_sorted, actual_list


