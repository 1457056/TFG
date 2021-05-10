import json
import test_texts as tp
import pickle
import tweepy as tw
import pandas as pd
import process_texts as pt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from pymongo import MongoClient
import prepare_out_texts as pot
from bson.codec_options import CodecOptions

client = MongoClient('localhost')

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
    """
    Método que utiliza la API de Twitter para descargar un conjunto de tweets a analizar
    :param search_keyword: Usuario, palabra o #
    :return:
    """
    try:
        api = getApi()

        if '@' in search_keyword:
            tweets_fetched = api.user_timeline(screen_name=search_keyword, since=start_date,
                                               until=end_date, count=num)
            return [{"text": status.text, "label": None} for status in tweets_fetched]
        else:
            tweets_fetched = tw.Cursor(api.search, search_keyword, since=start_date,
                                       until=end_date).items(num)
            return [{"text": status.text, "label": None} for status in tweets_fetched]

    except:
        print("Unfortunately, something went wrong..")
        return None


# ------------------------------------------------------------------------

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


def main(search_term, num, start, end):
    testDataSet = buildTestSet(search_term, num, start, end)
    result_df = pot.build_result_df(testDataSet, data_classified)
    max_tweets = pot.top_texts(result_df)
    result_json = df_to_json(max_tweets)
    return (result_json, result_df)
