import pickle
import test_texts as tp
import process_texts as pt

# Load the variables of the training
with open('Training results/logprior.pkl', 'rb') as f:
    logprior = pickle.load(f)
with open('Training results/loglikelihood.pkl', 'rb') as f:
    loglikelihood = pickle.load(f)

def build_result_df(testDataSet, data_classified):
    """
    Metodo que construye el dataframe resultante con el tweet, la polaridad y el rating
    :param data_classified:
    :return: data_classified
    """

    for tweet in testDataSet:
        p = tp.naive_bayes_predict(tweet['text'], logprior, loglikelihood)
        print(f'{tweet["text"]} -> {p:.2f}')

        data_classified = data_classified.append({
            'Tweet': pt.remove_usernames(tweet['text']),
            'Likes': int(tweet['likes']),
            'Label': label(p),
            'Rate': p
        }, ignore_index=True)
    return data_classified

def top_texts(result_df):
    new_df = result_df.sort_values('Rate')
    index = new_df.iloc[2:-2].index
    new_result_df = new_df.drop(index)
    return new_result_df

def label(p):
    """
    Método que a partir de la polaridad le asigna un rating
    :rtype: object
    """
    if p > 0.5:
        label = 'Positive'
    elif p <= 0.5 and p >= -0.5:
        label = 'Neutral'
    else:
        label = 'Negative'

    return label
