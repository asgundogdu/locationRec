from collections import Counter

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

def preprocess_binary():
	df_usa = pd.read_csv('data/yfcc_usa.csv')
	# Using only data in 2010s
	df_usa = df_usa[df_usa.date_taken.str.startswith('201')]
	# Converting time format
	df_usa['date_taken'] = pd.to_datetime(df_usa['date_taken'])
	# Removing year 2019 records as its wrongly labeled
	df_usa = df_usa[df_usa.date_taken < '2019-01-01']
	# Removing years has almost no records
	df_usa = df_usa[df_usa.date_taken < '2014-05-01']
	# Removing records without town infor
	df_usa = df_usa[~df_usa.town.isna()]

	# filtering values that has less check-in
	outlier_suburbs = []
	sub_counter = dict(Counter(df_usa.town.tolist()))
	for key in sub_counter.keys():
	    if sub_counter[key]<=100: outlier_suburbs.append(key)

	# filtering users that has less check-in
	outlier_users = []
	user_counter = dict(Counter(df_usa.user_nickname.tolist()))
	for key in user_counter.keys():
	    if user_counter[key]<=10: outlier_users.append(key)

	# Removing infrequent users and items
	df_usa = df_usa[~df_usa.town.isin(outlier_suburbs)]
	df_usa = df_usa[~df_usa.user_nickname.isin(outlier_users)]
	df_usa.shape

	# Train-Val-Test Split
	train = df_usa[['user_nickname', 'town', 'date_taken']][df_usa[['user_nickname', 'town', 'date_taken']].date_taken < '01-09-2012']
	validate = df_usa[['user_nickname', 'town', 'date_taken']][(df_usa[['user_nickname', 'town', 'date_taken']].date_taken <= '01-06-2013') &
	                                                (df_usa[['user_nickname', 'town', 'date_taken']].date_taken >= '01-09-2012')]
	test = df_usa[['user_nickname', 'town', 'date_taken']][df_usa[['user_nickname', 'town', 'date_taken']].date_taken > '01-06-2013']
	
	print(' train shape {}\n validation shape {}\n test shape {}'.format(train.shape,validate.shape,test.shape))

	# To avoid cold start problem
	all_towns = train.town.unique().tolist()
	all_users = train.user_nickname.unique().tolist()
	print(len(all_towns),len(all_users))

	#print(validate.shape)
	validate = validate[validate.town.isin(all_towns)]
	validate = validate[validate.user_nickname.isin(all_users)]
	#print(validate.shape)
	test = test[test.town.isin(all_towns)]
	test = test[test.user_nickname.isin(all_users)]

	# Creation of User Item Matrix
	user_item_df = pd.pivot_table(
	                        train[['user_nickname','town']], index=['user_nickname'], columns=['town'], aggfunc=len)
	#user_item_df = user_item_df.drop(outlier_suburbs,axis=1)
	#user_item_df = user_item_df.drop(outlier_users,axis=0)
	user_item_df = user_item_df.fillna(0.)
	# Binary check-ins
	user_item_df[user_item_df>0.] = 1.


	user_item_df.to_pickle('User_Item2.pckl')
	train.to_pickle('train2.pckl')
	validate.to_pickle('validate2.pckl')
	test.to_pickle('test2.pckl')


def preprocess_sum():
	df_usa = pd.read_csv('data/yfcc_usa.csv')
	# Using only data in 2010s
	df_usa = df_usa[df_usa.date_taken.str.startswith('201')]
	# Converting time format
	df_usa['date_taken'] = pd.to_datetime(df_usa['date_taken'])
	# Removing year 2019 records as its wrongly labeled
	df_usa = df_usa[df_usa.date_taken < '2019-01-01']
	# Removing years has almost no records
	df_usa = df_usa[df_usa.date_taken < '2014-05-01']
	# Removing records without town infor
	df_usa = df_usa[~df_usa.town.isna()]

	# filtering values that has less check-in
	outlier_suburbs = []
	sub_counter = dict(Counter(df_usa.town.tolist()))
	for key in sub_counter.keys():
	    if sub_counter[key]<=100: outlier_suburbs.append(key)

	# filtering users that has less check-in
	outlier_users = []
	user_counter = dict(Counter(df_usa.user_nickname.tolist()))
	for key in user_counter.keys():
	    if user_counter[key]<=10: outlier_users.append(key)

	# Removing infrequent users and items
	df_usa = df_usa[~df_usa.town.isin(outlier_suburbs)]
	df_usa = df_usa[~df_usa.user_nickname.isin(outlier_users)]
	df_usa.shape

	# Train-Val-Test Split
	train = df_usa[['user_nickname', 'town', 'date_taken']][df_usa[['user_nickname', 'town', 'date_taken']].date_taken < '01-09-2012']
	validate = df_usa[['user_nickname', 'town', 'date_taken']][(df_usa[['user_nickname', 'town', 'date_taken']].date_taken <= '01-06-2013') &
	                                                (df_usa[['user_nickname', 'town', 'date_taken']].date_taken >= '01-09-2012')]
	test = df_usa[['user_nickname', 'town', 'date_taken']][df_usa[['user_nickname', 'town', 'date_taken']].date_taken > '01-06-2013']
	
	print(' train shape {}\n validation shape {}\n test shape {}'.format(train.shape,validate.shape,test.shape))

	# To avoid cold start problem
	all_towns = train.town.unique().tolist()
	all_users = train.user_nickname.unique().tolist()
	print(len(all_towns),len(all_users))

	#print(validate.shape)
	validate = validate[validate.town.isin(all_towns)]
	validate = validate[validate.user_nickname.isin(all_users)]
	#print(validate.shape)
	test = test[test.town.isin(all_towns)]
	test = test[test.user_nickname.isin(all_users)]

	# Creation of User Item Matrix
	user_item_df = pd.pivot_table(
	                        train[['user_nickname','town']], index=['user_nickname'], columns=['town'], aggfunc=len)
	#user_item_df = user_item_df.drop(outlier_suburbs,axis=1)
	#user_item_df = user_item_df.drop(outlier_users,axis=0)
	user_item_df = user_item_df.fillna(0.)


	user_item_df.to_pickle('User_Item.pckl')
	train.to_pickle('train.pckl')
	validate.to_pickle('validate.pckl')
	test.to_pickle('test.pckl')