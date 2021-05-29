import json
import pandas as pd
from facebook_scraper import get_posts
import prepare_out_texts as pot


def buldTestSet(search_term,num):
    return [{"text": status['text'], "label": None, "likes": status['likes'],'comments':status['comments_full'], 'id': '2F'+status['post_id'], 'reactions':status['reactions']} for status in get_posts(search_term, pages=num, options={"comments": True, "reactors":True})]



def df_to_json(df_tweets):
    """
    Transforma el df en un excel y en un json para subirlo a mongo
    :param df_tweets: Df resultante de la predicción
    """
    df_tweets.to_json(r'D:\UAB\Uni\TFG\def_TFG\Facebook\df_fb.json', orient='split')

    with open(r'D:\UAB\Uni\TFG\def_TFG\Facebook\df_fb.json') as f:
        result = json.load(f)

    return result

data_classified = pd.DataFrame(columns=['Id','Tweet', 'Label', 'Rate','Comments','Reactions'])
data_classified_comments = pd.DataFrame(columns=['label'])

def main(search_term,num):
    testDataSet=buldTestSet(search_term,num)
    result_df,data_infrom = pot.build_result_df(testDataSet, data_classified,data_classified_comments)
    max_posts=pot.top_texts(result_df)
    result_json = df_to_json(max_posts)
    return(result_json, result_df, data_infrom)

