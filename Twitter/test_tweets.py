import json
import time

from Webpage import test_texts as tp
import pickle
import tweepy as tw
import pandas as pd
from Webpage import process_texts as pt
import matplotlib.pyplot as plt
from Webpage import prepare_out_texts as pot
from PIL import Image
import io
from os import remove
import base64

# initialize api instance
# Defining keys to access the Twitter API
consumer_key = 'ODQbnFsT1roZUSUzX9mRmzRaz'
consumer_secret = 'Uu3Qs0SxPYCWRT0aOp8QbCiQo1ojdt9H2c4NaoLBP4Q62gbB3u'
access_token = '1359827690610712579-LCAgiEhAxQkmTFEGZimqDZb515suCq'
access_token_secret = 'JZ41kNbD19oJVOAIIAfL3DFpxJBaviUlaAlmsnCZ20UbU'


def getApi():
    """
    Método que se autentica y devuelve la API de twitter
    :return:
    """
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    return api


# Run this cell to test your function
def buildTestSet(search_keyword, num, start_date, end_date):
    test_data = []
    API_LIMIT = 900
    """
    Método que utiliza la API de Twitter para descargar un conjunto de tweets a analizar
    :param search_keyword: Usuario, palabra o #
    :return:
    """
    try:
        api = getApi()
        new_num = num
        next = True
        rest = num
        count = 0

        while next:
            if num > 900:
                new_num = API_LIMIT
            count = new_num + count
            if '@' in search_keyword:
                tweets_fetched = api.user_timeline(screen_name=search_keyword, since=start_date,
                                                   until=end_date, count=new_num)
                test_data.append([{"text": status.text, "label": None, 'likes': status.favorite_count} for status in
                                  tweets_fetched])
            else:
                tweets_fetched = tw.Cursor(api.search, search_keyword, since=start_date,
                                           until=end_date).items(new_num)
                for status in tweets_fetched:
                    test_data.append({"text": status.text, "label": None, 'likes': status.favorite_count})
                    start_date = status.created_at
                    start_date = start_date.strftime('%Y-%m-%d')

            new_num = rest - new_num
            rest = new_num
            if rest == 0:
                next = False
            elif count == API_LIMIT:
                time.sleep(900)
        return test_data
    except:
        print("Unfortunately, something went wrong..")
        return None


# ------------------------------------------------------------------------

data_classified = pd.DataFrame(columns=['Tweet', 'Likes', 'Label', 'Rate'])


def df_to_json(df_tweets):
    """
    Transforma el df en un excel y en un json para subirlo a mongo
    :param df_tweets: Df resultante de la predicción
    """

    df_tweets.to_json('/home/gerard/Escritorio/TFG_deb/Webpage/Twitter/df_tw.json', orient='split')

    with open(r'/home/gerard/Escritorio/TFG_deb/Webpage/Twitter/df_tw.json') as f:
        result = json.load(f)

    return result


def main(search_term, num, start, end):
    testDataSet = buildTestSet(search_term, num, start, end)
    result_df = pot.build_result_df(testDataSet, data_classified)

    max_tweets = pot.top_texts(result_df)
    result_json = df_to_json(max_tweets)
    return (result_json, result_df)
