import process_texts as pt


# Predict Texts!
# UNQ_C4 (UNIQUE CELL IDENTIFIER, DO NOT EDIT)
def naive_bayes_predict(tweet, logprior, loglikelihood):
    '''
    Input:
        tweet: a string
        logprior: a number
        loglikelihood: a dictionary of words mapping to numbers
    Output:
        p: the sum of all the logliklihoods of each word in the tweet (if found in the dictionary) + logprior (a number)

    '''

    # process the tweet to get a list of words
    new_tweet = pt.translate_new_tweets(tweet)
    word_l = pt.process_tweet(new_tweet)

    # initialize probability to zero
    p = 0

    # add the logprior
    p += logprior

    for word in word_l:

        # get log likelihood of each keyword
        if word in loglikelihood:
            p += loglikelihood[word]

    return p
