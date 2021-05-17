from wordcloud import WordCloud, ImageColorGenerator
import base64
import os
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, send_from_directory, current_app, send_file
import flask
import pickle
import itertools
from os import remove
import graphics as grph
import time
from PIL import Image
import io
from os import remove
import base64
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Initialize the flask App


app = Flask(__name__)


def wordcloud_texts(texts):
    """
    Metodo para crear el wordcloud
    :param texts:
    :return:
    """
    stopwords = (['AT_USER', 'https', 'RT'])
    all_headlines = ' '.join(texts['Tweet'].str.lower())

    wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=1000).generate(all_headlines)
    wordcloud.to_file('/home/gerard/Escritorio/TFG_deb/Webpage/static/images/wordcloud.jpg')

    im = Image.open('/home/gerard/Escritorio/TFG_deb/Webpage/static/images/wordcloud.jpg')
    data = io.BytesIO()
    im.save(data, "JPEG")

    # Then encode the saved image file.
    encoded_img_data = base64.b64encode(data.getvalue())
    return encoded_img_data


def circular_graphic(tweets):
    """
    Metodo que crea el gráfico de pastel
    @param tweets:
    @return:
    """
    tweets['Label'].value_counts().plot(kind='pie', autopct='%.2f%%', title='Posts')

    plt.savefig('/home/gerard/Escritorio/TFG_deb/Webpage/static/images/circular_graph.jpg')

    im = Image.open('/home/gerard/Escritorio/TFG_deb/Webpage/static/images/circular_graph.jpg')
    data = io.BytesIO()
    im.save(data, "JPEG")

    # Then encode the saved image file.
    encoded_img_data_circular_graph = base64.b64encode(data.getvalue())
    return encoded_img_data_circular_graph


def excel(dframe, type):
    """
    Metodo que crea un excel con el análisis para descargarlo posteriormente
    @param dframe:
    @param type:
    """
    if type == 'twitter':
        dframe.to_excel('/home/gerard/Escritorio/TFG_deb/Webpage/Twitter/df_tw.xlsx')
    else:
        dframe.to_excel('/home/gerard/Escritorio/TFG_deb/Webpage/Facebook/df_fb.xlsx')


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
    # TODO: comprobar si existe usuario
    if flask.request.method == 'POST':
        # For rendering results on HTML GUI
        input_text = request.form['word']
        input_number = 20  # Tweets a descargar por defecto
        input_date_start = ''
        input_date_end = ''

        if 'twitter' in request.form:
            from Twitter import test_tweets as tt

            if 'number' in request.form:
                input_number = int(request.form['number'])
                input_date_start = request.form['start']
                input_date_end = request.form['end']

            prediction, texts = tt.main(input_text, input_number, input_date_start, input_date_end)
            excel(texts, 'twitter')
            wordcloudpic = wordcloud_texts(texts)
            graphic = circular_graphic(texts)



        elif 'facebook' in request.form:
            from Facebook import test_fb_posts as tf

            if 'number' in request.form:
                input_number = int(request.form['number'])

            prediction, texts = tf.main(input_text, input_number)

            wordcloudpic = wordcloud_texts(texts)
            graphic = circular_graphic(texts)

    return render_template('/base/predict.html', prediction_text=prediction['data'],
                           wordcloud=wordcloudpic.decode('utf-8'), graphic=graphic.decode('utf-8'))


@app.route('/download')
def download_file():
    """
    Método para descargar excel con análisis
    @return:
    """
    path = "/home/gerard/Escritorio/TFG_deb/Webpage/Twitter/df_tw.xlsx"
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
