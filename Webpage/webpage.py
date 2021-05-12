# import libraries
import base64
import io
import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from flask import Flask, render_template, request
import flask
import pickle
import itertools
from os import remove

# Initialize the flask App
from wordcloud import STOPWORDS, WordCloud

app = Flask(__name__)


def wordcloud(texts):
    """
    Metodo para crear el wordcloud
    :param texts:
    :return:
    """
    stopwords= (['AT_USER','https','RT']) + list(STOPWORDS)
    all_headlines = ' '.join(texts['Tweet'].str.lower())

    wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=1000).generate(all_headlines)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(r'C:\Users\Usuario\Desktop\TFG_last\Webpage\static\images\wordcloud.jpg')

    im = Image.open(r'C:\Users\Usuario\Desktop\TFG_last\Webpage\static\images\wordcloud.jpg')
    data = io.BytesIO()
    im.save(data, "JPEG")

    # Then encode the saved image file.
    encoded_img_data = base64.b64encode(data.getvalue())
    return encoded_img_data


def circular_graphic(tweets):
    tweets['Label'].value_counts().plot(kind='pie', autopct='%.2f%%', title='Posts')

    plt.savefig(r'C:\Users\Usuario\Desktop\TFG_last\Webpage\static\images\circular_graph.jpg')

    im = Image.open(r'C:\Users\Usuario\Desktop\TFG_last\Webpage\static\images\circular_graph.jpg')
    data = io.BytesIO()
    im.save(data, "JPEG")

    # Then encode the saved image file.
    encoded_img_data_circular_graph = base64.b64encode(data.getvalue())
    return encoded_img_data_circular_graph


# default page of our web-app
@app.route('/')
def home():
    return render_template('/Child/input_rrss.html')


# To use the predict button in our web-app

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
        input_number = 20 #Tweets a descargar por defecto
        input_date_start = ''
        input_date_end = ''

        if 'number'in request.form:
            input_number = int(request.form['number'])
            input_date_start = request.form['start']
            input_date_end = request.form['end']


        if 'twitter' in request.form:
            from Twitter import test_tweets as tt




            prediction, tweets = tt.main(input_text, input_number,input_date_start,input_date_end)
            encoded_img_data = wordcloud(tweets)
            graphic = circular_graphic(tweets)

        elif 'facebook' in request.form:
            from Facebook import test_fb_posts as tf
            prediction, tweets = tf.main(input_text, input_number)
            encoded_img_data = wordcloud(tweets)
            graphic = circular_graphic(tweets)

        return render_template('/Base/predict.html', prediction_text=prediction['data'],
                               image=encoded_img_data.decode('utf-8'), graphic=graphic.decode('utf-8'))


@app.route('/input_type_tw', methods=['GET'])
def input_type_tw():
    text = "de Twitter"
    type_rrss = "twitter"
    return render_template('Child/input_type_tw.html', text_title=text, type_rrss=type_rrss)

@app.route('/input_type_fb', methods=['GET'])
def input_type_fb():
    text = "de Facebook"
    type_rrss = "facebook"
    return render_template('Child/input_type_fb.html', text_title=text, type_rrss=type_rrss)


@app.route('/form', methods=['POST'])
def form():

    type_rrss = 'twitter'
    text_title = "de Twitter"
    if request.form['twitter']=='0':
        text = "Introduce una palabra o un hasgtag"
        type = "word"
    else:
        text = "Introduce un nombre de usuario"
        type = "user"
    return render_template('Child/form.html',text_title=text_title, text=text, type=type, type_rrss=type_rrss)


if __name__ == "__main__":
    app.run(debug=True)
