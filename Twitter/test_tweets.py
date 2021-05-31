import json
import time

import webpage as web
import tweepy as tw
import pandas as pd

import prepare_out_texts as pot


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
    """
    Método que utiliza la API de Twitter para descargar un conjunto de tweets a analizar
    :param search_keyword:
    :param num:
    :param start_date:
    :param end_date:
    :return:
    """
    test_data = []
    API_LIMIT = 900
    try:
        api = getApi()
        new_num = num
        next = True
        rest = num
        count = 0
        since_id=''

        while next:
            if new_num > 900:
                new_num = API_LIMIT
            else:
                new_num=rest
            count = new_num + count
            if '@' in search_keyword:

                tweets_fetched = api.user_timeline(screen_name=search_keyword, since=start_date,
                                                   until=end_date,count=new_num,include_rts=False)
                for status in tweets_fetched:
                    test_data.append({"text": status.text, "label": None,'id':status.id})
                    since_id = status.id
            else:
                tweets_fetched = tw.Cursor(api.search, search_keyword+'-filter:retweets', since=start_date,
                                           until=end_date,since_id=since_id, include_rts=False).items(new_num)
                for status in tweets_fetched:
                    test_data.append({"text": status.text, "label": None,'id':status.id})
                    since_id = status.id


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

data_classified = pd.DataFrame(columns=['Id','Tweet', 'Label', 'Rate','Comments'])


def df_to_json(df_tweets):
    """
    Transforma el df en un excel y en un json para subirlo a mongo
    :param df_tweets: Df resultante de la predicción
    """

    df_tweets.to_json(r'D:\UAB\Uni\TFG\def_TFG\Twitter\df_tw.json', orient='split')

    with open(r'D:\UAB\Uni\TFG\def_TFG\Twitter\df_tw.json') as f:
        result = json.load(f)

    return result


def main(search_term, num, start, end):
    testDataSet = buildTestSet(search_term, num, start, end)
    result_df,inform = pot.build_result_df(testDataSet, data_classified,None,'tw')
    max_tweets = pot.top_texts(result_df)
    result_json = df_to_json(max_tweets)
    return (result_json, result_df,inform)
