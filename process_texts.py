# ------PREPROCESS TEXTS------
import re  # library for regular expression operations
import string  # for string operations
import nltk
from nltk.corpus import stopwords  # module for stop words that come with NLTK
from nltk.stem import PorterStemmer  # module for stemming
from nltk.tokenize import TweetTokenizer  # module for tokenizing strings
from google_trans_new import google_translator

translator = google_translator()


def remove_usernames(tweet):
    """
    Metodo que usando expresiones regulares sustituye el nombre del usuario por AT_USER
    :param tweet:
    :return:
    """
    new_tweet = re.sub('@[^\s]+', 'AT_USER', tweet)  # remove usernames
    return new_tweet


def translate_new_tweets(tweet):
    """
    Método que traduce nuevos tweets
    :param tweet:
    :return:
    """
    new_tweet = translator.translate(tweet, lang_tgt='es')
    return new_tweet


def remove_hyperlinks_marks_styles(tweet):
    """
    Metodo que usando expresiones regulares elimina los hyperlinks
    :param tweet:
    :return:
    """
    new_tweet = re.sub(r'^RT[\s]+', '', tweet)

    # remove hyperlinks
    new_tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', new_tweet)

    # remove hashtags
    # only removing the hash # sign from the word
    new_tweet = re.sub(r'#', '', new_tweet)

    return new_tweet


# instantiate tokenizer class
tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                           reduce_len=True)


# Separate the tweet into individual words
def tokenize_tweet(tweet):
    """
    Método que tokeniza el tweet
    :param tweet:
    :return:
    """
    tweet_tokens = tokenizer.tokenize(tweet)

    return tweet_tokens


nltk.download('stopwords')

# Import the english stop words list from NLTK
stopwords_english = stopwords.words('spanish')
punctuations = string.punctuation


def remove_stopwords_punctuations(tweet_tokens):
    """
    Método que quita las stopwords y signos de puntuacion
    :param tweet_tokens:
    :return:
    """
    tweets_clean = []

    for word in tweet_tokens:
        if (word not in stopwords_english and word not in punctuations):
            tweets_clean.append(word)

    return tweets_clean


stemmer = PorterStemmer()


# Convert a word into its general form: learning -> learn
def get_stem(tweets_clean):
    """
    Metodo que simplifica las palabras -> aprendizaje -> aprender
    :param tweets_clean:
    :return:
    """
    tweets_stem = []

    for word in tweets_clean:
        stem_word = stemmer.stem(word)
        tweets_stem.append(stem_word)

    return tweets_stem


# return the tweet in the form of a list
def process_tweet(tweet):
    processed_tweet = remove_hyperlinks_marks_styles(tweet)
    tweet_tokens = tokenize_tweet(processed_tweet)
    tweets_clean = remove_stopwords_punctuations(tweet_tokens)
    tweets_stem = get_stem(tweets_clean)

    return tweets_stem
