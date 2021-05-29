import pickle
import test_texts as tp
import process_texts as pt
import pandas as pd

# Load the variables of the training
with open(r'D:\UAB\Uni\TFG\def_TFG\Training results\logprior.pkl', 'rb') as f:
    logprior = pickle.load(f)
with open(r'D:\UAB\Uni\TFG\def_TFG\Training results\loglikelihood.pkl', 'rb') as f:
    loglikelihood = pickle.load(f)

data_classified_comments = pd.DataFrame(columns=['Comentarios'])


def build_result_df(testDataSet, data_classified, data_comments):
    """
    Metodo que construye el dataframe resultante con el tweet, la polaridad y el rating
    :param data_classified:
    :return: data_classified
    """

    for text in testDataSet:
        p = tp.naive_bayes_predict(text['text'], logprior, loglikelihood)
        print(f'{text["text"]} -> {p:.2f}')
        data_comments = comments(text, data_comments)
        data_classified = data_classified.append({
            'Id': (text['id']),
            'Tweet': pt.remove_usernames(text['text']),
            'Label': label(p),
            'Rate': p,
            'Comments': "",
            'Pos_com': get_pos(data_comments),
            'Neg_com': get_neg(data_comments),
            'Neu_com': get_neu(data_comments),
        }, ignore_index=True)
        try:
            for comment in text['comments']:
                data_classified = data_classified.append({
                    'Comments': comment['comment_text']
                }, ignore_index=True)
        except:
            continue

    data_classified['Comments'] = data_classified['Comments'].shift(periods=-1)

    data_inform = data_classified
    data_classified = data_classified.drop(['Comments'], axis=1)
    data_classified = data_classified[data_classified['Id'].notna()]

    return data_classified, data_inform


def top_texts(result_df):
    """
    Metodo que coge los dos textos mas pos y neg
    :param result_df: dataframe con todos los textos
    :return: devuelve el df con los textos mas relevantes
    """
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
    elif 0.5 >= p >= -0.5:
        label = 'Neutral'
    elif p < -0.5:
        label = 'Negative'

    return label


def comments(text, df_comments):
    """
    Metodo que calcula el sentimiento de los comentarios de un solo post
    :param text: testo del post que contiene comentarios
    :param df_comments: dataframe con la probabilidad de los comentarios de un texto
    :return:
    """
    try:
        for comment in text['comments']:
            p = tp.naive_bayes_predict(comment['comment_text'], logprior, loglikelihood)
            df_comments = df_comments.append({
                'label': label(p)
            }, ignore_index=True)
        return df_comments
    except:
        return 0


def get_pos(data_comments):
    """
    Metodo que calcula el % de comentarios positivos de un post
    :param data_comments:
    :return:
    """
    pos = 0
    try:
        for label in data_comments['label']:
            if label == 'Positive':
                pos = pos + 1
        percentage = (pos / data_comments.shape[0]) * 100
        percentage = round(percentage, 2)
        return percentage
    except:
        return 0


def get_neg(data_comments):
    """
    Metodo que calcula el % de comentarios negativos de un post
    :param data_comments:
    :return:
    """
    neg = 0
    try:
        for label in data_comments['label']:
            if label == 'Negative':
                neg = neg + 1
        percentage = (neg / data_comments.shape[0]) * 100
        percentage = round(percentage, 2)
        return percentage

    except:
        return 0


def get_neu(data_comments):
    """
    Metodo que calcula el % de comentarios neutrales de un post
    :param data_comments:
    :return:
    """
    neu = 0
    try:
        for label in data_comments['label']:
            if label == 'Neutral':
                neu = neu + 1
        percentage = (neu / data_comments.shape[0]) * 100
        percentage = round(percentage, 2)
        return percentage
    except:
        return 0
