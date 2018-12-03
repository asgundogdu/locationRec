import pandas as pd
import numpy as np
import json
# from collections import Counter
# import tqdm
# import math
# from sklearn.metrics import mean_squared_error

from CF.collaborative_filtering import locationRec

from flask import Flask, jsonify
from flask_cors import CORS
import googlemaps
GOOGLE_MAP_KEY = <GOOGLEMAPKEY>

app = Flask(__name__)
CORS(app)

@app.route('/cf_eval/preprocessing=<p>&model=<m>&dim=<dim>&top_k=<topK>', methods=['GET'])
def cf_eval(p, m, dim, topK):
    json1_file = open('data/ht-data.json')
    json1_str = json1_file.read()
    json1_data = json.loads(json1_str)
    pre_calc_models = [(trial['Model'],trial['Preprocessing'],trial['LatentDimensions']) for trial in json1_data]
    dim = int(dim)
    topK = int(topK)

    p_dict = {'Numeric':1, 'Binary':2}
    m_dict = {'SVD_explicit':'SVD', 'SVD_implicit':'SVD_implicit'}

    print("p:{}-m:{}-dim:{}-topK:{}".format(p_dict[p], m_dict[m], dim, topK))
    recmodel = locationRec()
    recmodel.datapipeline(preproccesing=p_dict[p])

    # If given model hyperparameter is before evaluated and saved in 'data/ht-data.json' file
    if (m, p, dim) in pre_calc_models:
        if m_dict[m]=='SVD':
            recmodel.train_model(model_type=m_dict[m], latent_dimension=dim, N=topK)
        elif m_dict[m]=='SVD_implicit':
            recmodel.train_model(model_type=m_dict[m], latent_dimension=dim, N=topK, evaluate=False)

        print('+'*10)
        print((m, p, dim))
        print(pre_calc_models.index((m, p, dim)))
        print(pre_calc_models)
        print('-'*10, type(json1_data[pre_calc_models.index((m, p, dim))]['precision_train']))

        (recmodel.precision_train, recmodel.recall_train, recmodel.precision_val, \
                                 recmodel.recall_val, recmodel.rmse_train, recmodel.rmse_val) = (json1_data[pre_calc_models.index((m, p, dim))]['precision_train'], 
                                                                                                 json1_data[pre_calc_models.index((m, p, dim))]['recall_train'], 
                                                                                                 json1_data[pre_calc_models.index((m, p, dim))]['precision_val'], 
                                                                                                 json1_data[pre_calc_models.index((m, p, dim))]['recall_val'], 
                                                                                                 json1_data[pre_calc_models.index((m, p, dim))]['rmse_train'], 
                                                                                                 json1_data[pre_calc_models.index((m, p, dim))]['rmse_val'])

    # Evaluate the new model setup
    else:

        print('New model evaluation will take a while to loop over each user and locations')

        if m_dict[m]=='SVD':
            recmodel.train_model(model_type=m_dict[m], latent_dimension=dim, N=topK)
            recmodel.eval_precision_N(N=topK, data = 'train')
            recmodel.eval_precision_N(N=topK, data = 'val')
            recmodel.eval_rmse(data = 'train')
            recmodel.eval_rmse(data = 'val')
        elif m_dict[m]=='SVD_implicit':
            recmodel.train_model(model_type=m_dict[m], latent_dimension=dim, N=topK)

        data = [{"Model":m,
                "Preprocessing":p,
                "LatentDimensions":dim,
                "precision_train":pT,
                "recall_train":rT,
                "precision_val":pV,
                "recall_val":rV,
                "rmse_train":rmseT,
                "rmse_val":rmseV} for pT,rT,pV,rV,rmseT,rmseV in zip(recmodel.precision_train, recmodel.recall_train, recmodel.precision_val, 
                                                                     recmodel.recall_val, recmodel.rmse_train, recmodel.rmse_val)]

        json1_data += data

    print('Model:{} ,Preprocessing:{}, LatentDimensions:{}, Evaluate by Top {} Recommendations'.format(m,p_dict[p],dim,topK))
    print('recmodel.precision_train: {}\nrecmodel.recall_train: {}\nrecmodel.precision_val: {}\nrecmodel.recall_val: {}\nrecmodel.rmse_train: {}\nrecmodel.rmse_val: {}'.format(recmodel.precision_train, recmodel.recall_train, recmodel.precision_val, recmodel.recall_val, recmodel.rmse_train, recmodel.rmse_val))
    print()

    return jsonify(json1_data)


@app.route('/cf_recommend/preprocessing=<p>&model=<m>&dim=<dim>&top_k=<topK>&user=<user_id>', methods=['GET'])
def cf_recommend(p, m, dim, topK, user_id):
   
    dim = int(dim)
    topK = int(topK)

    p_dict = {'Numeric':1, 'Binary':2}
    m_dict = {'SVD_explicit':'SVD', 'SVD_implicit':'SVD_implicit'}

    print("p:{}-m:{}-dim:{}-topK:{}".format(p_dict[p], m_dict[m], dim, topK))
    recmodel = locationRec()
    recmodel.datapipeline(preproccesing=p_dict[p])

    if m_dict[m]=='SVD':
        recmodel.train_model(model_type=m_dict[m], latent_dimension=dim, N=topK)
    elif m_dict[m]=='SVD_implicit':
        recmodel.train_model(model_type=m_dict[m], latent_dimension=dim, N=topK, evaluate=False)
    id2user = dict(zip(list(range(recmodel.validate.user_nickname.nunique())), recmodel.validate.user_nickname.unique().tolist()))
    recommended_list_sorted, actual_list = recmodel.recommend_N_cities_for_user(topK, id2user[int(user_id)], data='val')
    print('recommended_list_sorted lenght: ',len(recommended_list_sorted))
    print('actual_list lenght: ',len(list(set(actual_list))))
    gmaps = googlemaps.Client(key=GOOGLE_MAP_KEY)


    recs_all = [{'Recommendations':rec, 'lat':get_LatLon(gmaps=gmaps, _input_=rec, _type_='lat'),
    			'lon':get_LatLon(gmaps=gmaps, _input_=rec, _type_='lng')} for rec in recommended_list_sorted if get_LatLon(gmaps=gmaps, _input_=rec)!='False']
    acts_all =  [{'Actuals':act, 'lat':get_LatLon(act, 'lat'),
    			'lon':get_LatLon(gmaps=gmaps, _input_=act, _type_='lng')} for act in list(set(actual_list)) if get_LatLon(gmaps=gmaps, _input_=act)!='False']
    
    return jsonify(recs_all + acts_all)


def get_LatLon(gmaps, _input_, _type_='lat'):
	return gmaps.geocode(_input_ + ', USA')[0]['geometry']['location'][_type_]
	# try:
	# 	return gmaps.geocode(_input_ + ', USA')[0]['geometry']['location'][_type_]
	# except:
	# 	print('exception!!!')
	# 	return 'False'



if __name__ == '__main__':
    app.run(debug=True, port=8090)

