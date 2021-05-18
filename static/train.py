import pickle
import process_texts as pt
import numpy as np

# Load the traductions
with open('new_all_negative_tweets.pkl', 'rb') as f:
    new_all_negative_tweets = pickle.load(f)
with open('new_all_positive_tweets.pkl', 'rb') as f:
    new_all_positive_tweets = pickle.load(f)


# Clean the tweets that may have traduced twice
def filter(list_tweets):
    """
    Metodo que corrige traducciones dobles
    :param list_tweets:
    :return:
    """
    for index, item in enumerate(list_tweets):
        if isinstance(item, list):
            print(item)
            list_tweets[index] = item[0]
    return list_tweets


new_all_negative_tweets = filter(new_all_negative_tweets)
new_all_positive_tweets = filter(new_all_positive_tweets)

# Split data into two pieces, one for training and one for testing¶
test_pos = new_all_positive_tweets[2000:]
train_pos = new_all_positive_tweets[:2000]
test_neg = new_all_negative_tweets[2000:]
train_neg = new_all_negative_tweets[:2000]

train_x = train_pos + train_neg
test_x = test_pos + test_neg

train_y = np.append(np.ones(len(train_pos)), np.zeros(len(train_neg)))
test_y = np.append(np.ones(len(test_pos)), np.zeros(len(test_neg)))


def create_frequency(tweets, ys):
    """
    Método que crea un diccionnario de frecucencias
    Para cada palabra clave se le asigna un valor que será el número de veces que aparece
    Si la palabra malo aparece en un tweet negativo: (malo,0)
    Se añade al diccionario, si ya estaba se incrementa en 1 el número de veces que aparece ((malo,0),1)
    :param tweets:
    :param ys:
    :return:
    """
    freq_d = {}

    # tweet: string; y: tweet value 0/1
    for tweet, y in zip(tweets, ys):
        for word in pt.process_tweet(tweet):
            # for each key word we will asign that value if appears in the dict
            pair = (word, y)  # if the word is "bad" and appears in a neg tweet, the pair will be (bad,0)
            # Then we put the pair in the dictionary, if its already in, increment the value of the pair
            if pair in freq_d:
                freq_d[pair] += 1
            else:
                freq_d[pair] = freq_d.get(pair, 1)

    return freq_d


freqs = create_frequency(train_x, train_y)


def train_naive_bayes(freqs, train_x, train_y):
    '''
    Input:
        freqs: dictionary from (word, label) to how often the word appears
        train_x: a list of tweets
        train_y: a list of labels correponding to the tweets (0,1)
    Output:
        logprior: the log prior. (equation 3 above). Probability of a tweet being pos or neg. Needed to calculate the total probab
        loglikelihood: the log likelihood of you Naive bayes equation. (equation 6 above). Dictionary with the prob of a word being in a pos tweet vs in a neg tweet
    '''

    loglikelihood = {}
    logprior = 0

    # calculate the number of unique words in vocab
    unique_words = set([pair[0] for pair in freqs.keys()])
    V = len(unique_words)

    # calculate N_pos and N_neg. All pos word and neg
    N_pos = N_neg = 0
    for pair in freqs.keys():
        if pair[1] > 0:
            N_pos += freqs[(pair)]
        else:
            N_neg += freqs[(pair)]

    # TODO: calculate the number of documents (tweets)
    D = train_y.shape[0]

    # TODO: calculate D_pos, the number of positive documents (tweets)
    D_pos = sum(train_y)

    # TODO: calculate D_neg, the number of negative documents (tweets)
    D_neg = D - sum(train_y)

    # TODO: calculate logprior
    logprior = np.log(D_pos) - np.log(D_neg)

    # for each unqiue word
    for word in unique_words:
        # get the positive and negative frequency of the word
        freq_pos = freqs.get((word, 1), 0)
        freq_neg = freqs.get((word, 0), 0)

        # calculate the probability that word is positive, and negative
        p_w_pos = (freq_pos + 1) / (N_pos + V)
        p_w_neg = (freq_neg + 1) / (N_neg + V)

        # calculate the log likelihood of the word
        loglikelihood[word] = np.log(p_w_pos / p_w_neg)

    return logprior, loglikelihood


logprior, loglikelihood = train_naive_bayes(freqs, train_x, train_y)

# Save the training variables to use in the prediction
import _pickle as cPickle

with open('Training results/logprior.pkl', 'wb') as fp:
    cPickle.dump((logprior), fp, -1)
with open('Training results/loglikelihood.pkl', 'wb') as fp:
    cPickle.dump((loglikelihood), fp, -1)
