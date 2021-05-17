import json
import pandas as pd
from facebook_scraper import get_posts
from Webpage import prepare_out_texts as pot


def buldTestSet(search_term,num):
    return [{"text": status['text'], "label": None, "likes": status['likes']} for status in get_posts(search_term, pages=num, options={"reactors": True})]



def df_to_json(df_tweets):
    """
    Transforma el df en un excel y en un json para subirlo a mongo
    :param df_tweets: Df resultante de la predicción
    """
    df_tweets.to_json('/home/gerard/Escritorio/TFG_deb/Webpage/df_tw.json', orient='split')

    with open('/home/gerard/Escritorio/TFG_deb/Webpage/df_tw.json') as f:
        result = json.load(f)

    return result

data_classified = pd.DataFrame(columns=['Tweet', 'Likes', 'Label', 'Rate'])
def main(search_term,num):
    testDataSet=buldTestSet(search_term,num)
    result_df = pot.build_result_df(testDataSet, data_classified)
    max_posts=pot.top_texts(result_df)
    result_json = df_to_json(max_posts)
    return(result_json, result_df)

