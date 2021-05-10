import json
from pymongo import MongoClient
import test_texts as tp
import facebook as fb
import pickle
import pandas as pd
import os
import matplotlib.pyplot as plt
from facebook_scraper import get_posts
import prepare_out_texts as pot

client = MongoClient('localhost')


def buldTestSet(search_term,num):
    return [{"text": status['text'], "label": None} for status in get_posts(search_term, pages=num)]

data_classified = pd.DataFrame(columns=['Tweet', 'Label', 'Rate'])

def df_to_json(df_tweets):
    """
    Transforma el df en un excel y en un json para subirlo a mongo
    :param df_tweets: Df resultante de la predicción
    """
    df_tweets.to_excel(r'C:\Users\Usuario\Desktop\TFG_last\Twitter\df_tw.xlsx')
    df_tweets.to_json(r'C:\Users\Usuario\Desktop\TFG_last\Twitter\df_tw.json', orient='split')

    with open(r'C:\Users\Usuario\Desktop\TFG_last\Twitter\df_tw.json') as f:
        result = json.load(f)

    db = client['Result_dfs']
    col = db['dfs_twitter']
    col.insert_one(result)
    return result


def main(search_term,num):
    testDataSet=buldTestSet(search_term,num)
    result_df = pot.build_result_df(testDataSet, data_classified)
    max_posts=pot.top_texts(result_df)
    result_json = df_to_json(max_posts)
    return(result_json, result_df)

