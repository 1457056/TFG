import time
import _pickle as cPickle
import nltk
from nltk.corpus import twitter_samples
from google_trans_new import google_translator

nltk.download('twitter_samples')
translator = google_translator()


# select the set of positive and negative tweets
all_positive_tweets = twitter_samples.strings('positive_tweets.json')
all_negative_tweets = twitter_samples.strings('negative_tweets.json')
new_all_positive_tweets=[]
new_all_negative_tweets=[]


rate_limit = 180
sleep_time = 900 / 180
count=0

#Translate postive and negative tweets
for index,i in enumerate(all_positive_tweets[:2500]):
    new_all_positive_tweets.append(translator.translate(all_positive_tweets[index],lang_tgt='es'))
    time.sleep(sleep_time)
    count=count+1
    print(count)

time.sleep(3600)
for index,i in enumerate(all_negative_tweets[:2500]):
    new_all_negative_tweets.append(translator.translate(all_negative_tweets[index],lang_tgt='es'))
    time.sleep(sleep_time)
    count=count+1
    print(count)
    if count == 4000:
        time.sleep(900)

#Save the traduction
with open('../new_all_negative_tweets.pkl', 'wb') as fp:
    cPickle.dump((new_all_negative_tweets), fp, -1)
with open('../new_all_positive_tweets.pkl', 'wb') as fp:
    cPickle.dump((new_all_positive_tweets), fp, -1)

