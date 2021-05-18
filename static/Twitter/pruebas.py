from Twitter.test_tweets import getApi
import tweepy as tw

def buildTestSet(search_keyword,num,start_date,end_date):
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
            print(tweets_fetched)
            return [{"text": status.text, "label": None} for status in tweets_fetched]
        else:
            tweets_fetched = tw.Cursor(api.search, search_keyword, since=start_date,
            until=end_date).items(num)
            for status in tweets_fetched:
                print(status.text)
            return [{"text": status.text, "label": None} for status in tweets_fetched]

    except:
        print("Unfortunately, something went wrong..")
        return None

buildTestSet('hola',5,'','')