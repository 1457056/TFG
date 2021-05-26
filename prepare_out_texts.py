import pickle
import test_texts as tp
import process_texts as pt

# Load the variables of the training
with open(r'C:\Users\Usuario\Desktop\TFG\Training results\logprior.pkl', 'rb') as f:
    logprior = pickle.load(f)
with open(r'C:\Users\Usuario\Desktop\TFG\Training results\loglikelihood.pkl', 'rb') as f:
    loglikelihood = pickle.load(f)

def build_result_df(testDataSet, data_classified,data_comments):
    """
    Metodo que construye el dataframe resultante con el tweet, la polaridad y el rating
    :param data_classified:
    :return: data_classified
    """

    for tweet in testDataSet:
        p = tp.naive_bayes_predict(tweet['text'], logprior, loglikelihood)
        print(f'{tweet["text"]} -> {p:.2f}')
        data_comments=comments(tweet, data_comments)
        data_classified = data_classified.append({
            'Tweet': pt.remove_usernames(tweet['text']),
            'Label': label(p),
            'Rate': p,
            'Pos_com': get_pos(data_comments),
            'Neg_com': get_neg(data_comments),
            'Neu_com': get_neu(data_comments),
            'Id': (tweet['id'])
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

def comments(tweet,df_comments):
    try:
        for comment in tweet['comments']:
            p = tp.naive_bayes_predict(comment['comment_text'], logprior, loglikelihood)
            df_comments=df_comments.append({
                'label': label(p)
            },ignore_index=True)
        return df_comments
    except:
        return 0

def get_pos(data_comments):
    pos = 0
    try:
        for label in data_comments['label']:
            if label=='Positive':
                pos = pos +1
        percentage = (pos / data_comments.shape[0]) * 100
        percentage=round(percentage, 2)
        return percentage
    except:
        return 0

def get_neg(data_comments):
    neg = 0
    try:
        for label in data_comments['label']:
            if label == 'Negative':
                neg = neg + 1
        percentage=(neg / data_comments.shape[0]) * 100
        percentage=round(percentage, 2)
        return percentage

    except:
        return 0

def get_neu(data_comments):
    neu = 0
    try:
        for label in data_comments['label']:
            if label == 'Neutral':
                neu = neu + 1
        percentage=(neu / data_comments.shape[0]) * 100
        percentage=round(percentage, 2)
        return percentage
    except:
        return 0