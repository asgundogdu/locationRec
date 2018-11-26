#!/usr/bin/python

# Imports

import pandas as pd
import numpy as np
from collections import Counter
import tqdm
import math, os
from sklearn.metrics import mean_squared_error
from scipy.sparse.csgraph import minimum_spanning_tree as mst_nsim
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix
from scipy import sparse 
import implicit

from .data import preprocess_binary

# Methods
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


def svd_model(user_item_df, latent_dimension, N):
    Checkins_demeaned = user_item_df.values/np.mean(user_item_df.values)
    U, sigma, Vt = svds(Checkins_demeaned, latent_dimension)
    sigma = np.diag(sigma)
    all_user_predicted_checkins = np.dot(np.dot(U, sigma), Vt) + np.mean(user_item_df.values)
    preds = pd.DataFrame(all_user_predicted_checkins, columns = user_item_df.columns, index=user_item_df.index)
    return preds


def implicit_model(user_item_df, train, validate, latent_dimension, N, preproccesing):
    if preproccesing==2:
        validate = pd.DataFrame({'count' : validate.groupby(['user_nickname','town'])['town'].apply(len)}).reset_index()
        validate['count'] = [1]*validate.shape[0]

        train = pd.DataFrame({'count' : train.groupby(['user_nickname','town'])['town'].apply(len)}).reset_index()
        train['count'] = [1]*train.shape[0]
    elif preproccesing==1:
        validate = pd.DataFrame({'count' : validate.groupby(['user_nickname','town'])['town'].apply(len)}).reset_index()
        train = pd.DataFrame({'count' : train.groupby(['user_nickname','town'])['town'].apply(len)}).reset_index()

    # initialize a model
    model = implicit.als.AlternatingLeastSquares(factors=latent_dimension)
    # train the model on a sparse matrix of item/user/confidence weights
    #model.fit(csr_matrix(user_item_df.values.T))
    # recommend items for a user
    user_items = csr_matrix(user_item_df).T.tocsr()
    # get top N recommendations
    user_dict = dict(zip(list(range(len(user_item_df.index.tolist()))), user_item_df.index.tolist()))
    user_dict_inverse = dict(zip(user_item_df.index.tolist(), list(range(len(user_item_df.index.tolist())))))
    town_dict = dict(zip(list(range(len(user_item_df.columns.tolist()))), user_item_df.columns.tolist()))
    town_dict_inverse = dict(zip(user_item_df.columns.tolist(), list(range(len(user_item_df.columns.tolist())))))
    
    # recommend items for a user
    user_items = csr_matrix(user_item_df).T.tocsr()
    item_users = user_items.T

    # train the model on a sparse matrix of item/user/confidence weights
    print('Tranining model...')
    model.fit(user_items, show_progress=True)

    print('Computing RMSE for training set')
    rmse_train = rmse_implicit(user_dict, town_dict_inverse, model, user_item_df, train, item_users)
    print('Computing RMSE for validation set')
    rmse_valid = rmse_implicit(user_dict, town_dict_inverse, model, user_item_df, validate, item_users)

    print("Calculating precision, recall on training set")
    precisionN_train, recallN_train = prec_recall_implicit(user_dict, town_dict_inverse, town_dict, model, train, item_users, N)
    print("Calculating precision, recall on validation set")
    precisionN_val, recallN_val = prec_recall_implicit(user_dict, town_dict_inverse, town_dict, model, validate, item_users, N)
    # tp, fp, fn = 0., 0., 0.
    # for userid in tqdm.tqdm(list(user_dict.keys())[:3000], total=len(list(user_dict.keys())[:3000]),position=0):
    #     recs = model.recommend(userid, item_users, N=N)
    #     gt = validate[validate.user_nickname==user_dict[userid]].town.unique().tolist()
    #     for enum, recomendation in enumerate(recs):
    #         if enum == len(gt): break  
    #         if town_dict[recomendation[0]] in gt:
    #             tp += 1.
    #         elif town_dict[recomendation[0]] not in gt:
    #             fp += 1.

    #     for real in gt:
    #         if town_dict_inverse[real] not in [r[0] for r in recs]:
    #             fn += 1.
    # print('tp:{}, fp:{}, fn:{}'.format(tp,fp,fn))
    # precisionN = tp/(tp+fp)
    # recallN = tp/(tp+fn)

    return model, precisionN_train, recallN_train, precisionN_val, recallN_val, rmse_train, rmse_valid


def prec_recall_implicit(user_dict, town_dict_inverse, town_dict, model, validate, item_users, N):
    tp, fp, fn = 0., 0., 0.
    for userid in tqdm.tqdm(list(user_dict.keys())[:3000], total=len(list(user_dict.keys())[:3000]),position=0):
        recs = model.recommend(userid, item_users, N=N)
        gt = validate[validate.user_nickname==user_dict[userid]].town.unique().tolist()
        for enum, recomendation in enumerate(recs):
            if enum == len(gt): break  
            if town_dict[recomendation[0]] in gt:
                tp += 1.
            elif town_dict[recomendation[0]] not in gt:
                fp += 1.

        for real in gt:
            if town_dict_inverse[real] not in [r[0] for r in recs]:
                fn += 1.
    print('tp:{}, fp:{}, fn:{}'.format(tp,fp,fn))
    precisionN = tp/(tp+fp)
    recallN = tp/(tp+fn)
    return precisionN, recallN


def rmse_implicit(user_dict, town_dict_inverse, model, user_item_df, validate, item_users):
    rmse_pred, rmse_gt = [],[]
    for userid in list(user_dict.keys())[:3000]:
        recs = model.recommend(userid, item_users, N=len(user_item_df.columns.tolist()))
        gt = validate[validate.user_nickname==user_dict[userid]]#.town.unique().tolist()
        if len(gt)==0: continue
        for ind, row in gt.iterrows():
            try:
                pred_val = recs[[r[0] for r in recs].index(town_dict_inverse[row['town']])][1]
            except:
                print(ValueError, row['town'])
                continue
            rmse_gt.append(row['count'])
            rmse_pred.append(pred_val)
    rmse = math.sqrt(mean_squared_error(rmse_gt, rmse_pred))
    return rmse


# Class

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
        self.preproccesing = None


    def datapipeline(self, preproccesing=1):
        self.preproccesing = preproccesing
        if preproccesing==1:
            self.user_item_df = pd.read_pickle('User_Item.pckl')
            self.train = pd.read_pickle('train.pckl')
            self.validate = pd.read_pickle('validate.pckl')
            self.test = pd.read_pickle('test.pckl')
        if preproccesing==2:
            if os.path.isfile('User_Item2.pckl') and os.path.isfile('train2.pckl') and os.path.isfile('validate2.pckl') and os.path.isfile('test2.pckl'):
                pass
            else:
                preprocess_binary()
            self.user_item_df = pd.read_pickle('User_Item2.pckl')
            self.train = pd.read_pickle('train2.pckl')
            self.validate = pd.read_pickle('validate2.pckl')
            self.test = pd.read_pickle('test2.pckl')


    def train_model(self, model_type='SVD', latent_dimension=50, N=10):
        if model_type == 'SVD':
            print('Training using SVD model...')
            self.preds = svd_model(self.user_item_df, latent_dimension, N)
        elif model_type == 'SVD_implicit':
            print('Training using SVD_implicit model...')
            #self.preds = implicit_model(self.user_item_df, self.train, self.validate, latent_dimension, N, self.preproccesing)
            self.model, self.precision_train, self.recall_train, self.precision_val, self.recall_val, self.rmse_train, self.rmse_val = \
                                implicit_model(self.user_item_df, self.train, self.validate, latent_dimension, N, self.preproccesing)
            #TODO compute self.preds using self.model
        elif model_type == 'AutoEncoder':
            pass
        print('Done')


    def eval_rmse(self, data='val'):
        if data == 'val':
            self.rmse_val = compute_rmse(self.preds, self.validate)
        elif data == 'train':
            self.rmse_train = compute_rmse(self.preds, self.train)
        elif data == 'test':
            self.rmse_test = compute_rmse(self.preds, self.test)


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
            actual_list = val_user_df.town.tolist()
        if data=='test':
            val_user_df = self.test[self.test.user_nickname == user]
            actual_list = val_user_df.town.tolist()

        return recommended_list_sorted, actual_list


