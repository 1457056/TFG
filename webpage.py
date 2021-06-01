import copy

import cv2
import imutils
from flask import Flask, render_template, request, send_from_directory, current_app, send_file
import flask
import matplotlib
import nltk
from nltk.corpus import stopwords
import seaborn as sns
import prepare_out_texts as pot
from stop_words import get_stop_words

sns.set()
import stylecloud

nltk.download('stopwords')
stop_words_sp = list(stopwords.words('spanish'))
stop_words_en = list(stopwords.words('english'))
stop_words_ca = get_stop_words('catalan')
stop_words_spa = get_stop_words('spanish')
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Initialize the flask App


app = Flask(__name__)

with open(r"D:\UAB\Uni\TFG\def_TFG\static\stopwords_sp", "r") as f:
    stopw_sp = [line.strip() for line in f]

with open(r"D:\UAB\Uni\TFG\def_TFG\static\stopwords-ca.txt", "r") as f:
    stopw_ca = [line.strip() for line in f]


def wordcloud_texts(texts, type):
    """
    Metodo para crear el wordcloud
    Si es para Twitter se crea normal, con los tweets obtenidos
    Si es para facebook se recorren los comentarios de cada post, creando un wordcloud para cada uno de ellos
    :param texts:
    :return:
    """

    stopwords = (['AT_USER', 'https', 'RT', 'de', 'la', 'con', 'por', 'en', 'una', 'que', 'q', 'y', 'el', 'lo', 'se',
                  'a', 'un', 't', 'co', 'así','què','mes','més','perque','són','fet','lis',] + stop_words_sp + stopw_sp + stop_words_en + stopw_ca + stop_words_ca + stop_words_spa)

    if type == 'tw':
        my_mask = 'fas fa-cloud'
        all_headlines_tw = ' '.join(texts['Tweet'].str.lower())
        stylecloud.gen_stylecloud(all_headlines_tw, icon_name=my_mask,
                                  output_name=r'D:\UAB\Uni\TFG\def_TFG\static\images\tw_images\wordcloud.jpg',
                                  custom_stopwords=stopwords,
                                  collocations=False,
                                  max_words=1000)
    else:
        my_mask = 'fab fa-facebook'

        # Prepare data

        index_texts = texts
        index_texts = pot.top_texts(index_texts)
        texts = texts.sort_values('Rate')
        texts.reset_index(level=0, inplace=True)
        index_texts.reset_index(level=0, inplace=True)

        for index, id in enumerate(index_texts['Id']):
            id = index_texts['Id'][index]
            filter_comments = texts['Comments'][texts['Id'] == id]
            filter_comments = filter_comments[:-1]

            all_headlines_fb = ' '.join(filter_comments.str.lower())

            # SI no hay suficientes comentarios mostramos NOT ENOUGH DATA
            if len(filter_comments) <= 7:
                output_name = r'D:\UAB\Uni\TFG\def_TFG\static\images\fb_images\wordclouds\wordcloud' + str(
                    index) + '.jpg'
                img_src = cv2.imread(r'D:\UAB\Uni\TFG\def_TFG\static\images\not_data.png')

                cv2.imwrite(output_name, img_src)

            else:
                stylecloud.gen_stylecloud(all_headlines_fb, icon_name=my_mask,
                                          output_name=r'D:\UAB\Uni\TFG\def_TFG\static\images\fb_images\wordclouds\wordcloud' + str(
                                              index) + '.jpg',
                                          custom_stopwords=stopwords,
                                          collocations=False,
                                          max_words=1000
                                          )

    # wordcloud = WordCloud(stopwords=stopwords, mask=my_mask, contour_width=3,
    # contour_color='black', background_color="white", max_words=words).generate(all_headlines)
    # wordcloud.to_file(r'D:\UAB\Uni\TFG\def_TFG\static\images\wordcloud.jpg')


def circular_graphic(texts, type):
    """
    Metodo que crea el gráfico de pastel
    Si es para Twitter se crea normal, con los tweets obtenidos
    Si es para facebook se recorren los comentarios de cada post, creando un grafico para cada uno de ellos
    @param tweets:
    @return:
    """

    if type == 'tw':
        labels = []
        colors = []

        data = texts['Label'].value_counts()

        for i in data.index:
            labels.append(i)
            if i == 'Positive':
                colors.append('lightgreen')
            elif i == 'Negative':
                colors.append('lightcoral')
            elif i == 'Neutral':
                colors.append('lightblue')

        plt.figure()
        plt.pie(data, colors=colors, labels=labels, shadow=True, autopct='%.2f%%')
        plt.legend(loc="best")
        plt.axis('equal')
        plt.savefig(r'D:\UAB\Uni\TFG\def_TFG\static\images\tw_images\circular_graph.svg',
                    transparent=False)

        del data
        del labels
    else:
        index_texts = texts
        index_texts = pot.top_texts(index_texts)
        texts = texts.sort_values('Rate')
        texts.reset_index(level=0, inplace=True)
        index_texts.reset_index(level=0, inplace=True)

        for index, id in enumerate(index_texts['Id']):
            labels = []
            colors = []

            id = index_texts['Id'][index]
            filter_comments_label = texts['Comments label'][texts['Id'] == id]
            filter_comments_label = filter_comments_label[:-1]
            data = filter_comments_label.value_counts()

            for i in data.index:
                labels.append(i)
                if i == 'Positive':
                    colors.append('lightgreen')
                elif i == 'Negative':
                    colors.append('lightcoral')
                elif i == 'Neutral':
                    colors.append('lightblue')

            if len(labels) == 0:
                output_name = r'D:\UAB\Uni\TFG\def_TFG\static\images\fb_images\graphics\circular_graph' + str(
                    index) + '.jpg'
                img_src = cv2.imread(r'D:\UAB\Uni\TFG\def_TFG\static\images\nocomments.png')

                cv2.imwrite(output_name, img_src)

            else:
                plt.figure()
                plt.pie(data, colors=colors, labels=labels, shadow=True, autopct='%.2f%%')
                plt.legend(loc="best")
                plt.axis('equal')
                plt.savefig(
                    r'D:\UAB\Uni\TFG\def_TFG\static\images\fb_images\graphics\circular_graph' + str(index) + '.jpg',
                    transparent=False)

            del data
            del labels


def excel(dframe):
    """
    Metodo que crea un excel con el análisis para descargarlo posteriormente
    @param dframe:
    @param type:
    """
    dframe.to_excel(r'D:\UAB\Uni\TFG\def_TFG\Result_df\df_postss.xlsx')


# default page of our web-app
@app.route('/')
def home():
    return render_template('child/input_rrss.html')


@app.route('/input_type_tw', methods=['GET'])
def input_type_tw():
    text = "de Twitter"
    type_rrss = "twitter"
    return render_template('child/input_type_tw.html', text_title=text, type_rrss=type_rrss)


@app.route('/input_type_fb', methods=['GET'])
def input_type_fb():
    text = "de Facebook"
    type_rrss = "facebook"
    return render_template('child/input_type_fb.html', text_title=text, type_rrss=type_rrss)


@app.route('/form', methods=['POST'])
def form():
    type_rrss = 'twitter'
    text_title = "de Twitter"
    if request.form['twitter'] == '0':
        text = "Introduce una palabra o un hasgtag"
        type = "word"
    else:
        text = "Introduce un nombre de usuario"
        type = "user"
    return render_template('child/form.html', text_title=text_title, text=text, type=type, type_rrss=type_rrss)


@app.route('/predict', methods=['POST'])
def predict():
    """
    Método que cuando pulsmos el boton predict, inicia la predicción de textos
    en el backend, los recupera y los envía al front
    :return:
    """

    if flask.request.method == 'POST':
        # For rendering results on HTML GUI
        input_text = request.form['word']
        input_number = 50  # Tweets a descargar por defecto
        input_date_start = ''
        input_date_end = ''

        if 'twitter' in request.form:
            from Twitter import test_tweets as tt

            if 'number' in request.form:
                if request.form['number']:
                    input_number = int(request.form['number'])
                input_date_start = request.form['start']
                input_date_end = request.form['end']

            prediction, texts, inform = tt.main(input_text, input_number, input_date_start, input_date_end)

            excel(texts)
            wordcloud_texts(texts, 'tw')
            circular_graphic(texts, 'tw')

            return render_template('/base/predict.html', prediction_text=prediction['data'])


        elif 'facebook' in request.form:
            from Facebook import test_fb_posts as tf

            if 'number' in request.form:
                input_number = int(request.form['number'])

            prediction, texts, inform = tf.main(input_text, input_number)
            excel(inform)
            wordcloud_texts(texts, 'fb')
            circular_graphic(texts, 'fb')

            return render_template('/base/predict_fb.html', prediction_text=prediction['data'])


@app.route('/download_info')
def downloadFile():
    """
    Método para descargar excel con análisis
    @return:
    """
    path = "Result_df/df_postss.xlsx"
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
