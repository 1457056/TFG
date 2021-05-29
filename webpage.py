import datetime
import time
from os import remove
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator
from flask import Flask, render_template, request, send_from_directory, current_app, send_file
import flask
from PIL import Image
import io
import base64
import matplotlib
import nltk
from nltk.corpus import stopwords
from datetime import datetime
import seaborn as sns
sns.set()
import stylecloud

nltk.download('stopwords')
stop_words_sp = list(stopwords.words('spanish'))
stop_words_en = list(stopwords.words('english'))
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Initialize the flask App


app = Flask(__name__)

with open(r"D:\UAB\Uni\TFG\def_TFG\static\stopwords_sp", "r") as f:
    stopw_sp = [line.strip() for line in f]


def wordcloud_texts(texts, type):
    """
    Metodo para crear el wordcloud
    :param texts:
    :return:
    """
    stopwords = (['AT_USER', 'https', 'RT', 'de', 'la', 'con', 'por', 'en', 'una', 'que', 'q', 'y', 'el', 'lo', 'se',
                  'a', 'un', 't', 'co'] + stop_words_sp + stopw_sp + stop_words_en)
    all_headlines = ' '.join(texts['Tweet'].str.lower())

    if type == 'tw':
        my_mask = np.array(Image.open(r'D:\UAB\Uni\TFG\def_TFG\static\images\tw_logo.png'))
        words = 2000
    else:
        my_mask = np.array(Image.open(r'D:\UAB\Uni\TFG\def_TFG\static\images\fb_logo.png'))
        words = 1000

    wordcloud = WordCloud(stopwords=stopwords, mask=my_mask, contour_width=3,
                          contour_color='black', background_color="white", max_words=words).generate(all_headlines)
    wordcloud.to_file(r'D:\UAB\Uni\TFG\def_TFG\static\images\wordcloud.jpg')


    im = Image.open(r'D:\UAB\Uni\TFG\def_TFG\static\images\wordcloud.jpg')
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
    labels = ['Positive', 'Negative', 'Neutral']

    data = tweets['Label'].value_counts()
    plt.figure()
    plt.pie(data, colors=['yellowgreen', 'red', 'blue'], shadow=True, autopct='%.2f')
    plt.legend(labels)
    plt.axis('equal')
    now = datetime.now().timestamp()
    now = str(now)
    plt.savefig(r'D:\UAB\Uni\TFG\def_TFG\static\images\circular_graph.svg', transparent=False)

    del data
    del labels

    return now


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
    # TODO: comprobar si existe usuario
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
            wordcloudpic = wordcloud_texts(texts, 'tw')
            #remove('static/images/circular_graph.svg')
            circular_graphic(texts)

            return render_template('/base/predict.html', prediction_text=prediction['data'],
                                   wordcloud=wordcloudpic.decode('utf-8'))


        elif 'facebook' in request.form:
            from Facebook import test_fb_posts as tf

            if 'number' in request.form:
                input_number = int(request.form['number'])

            prediction, texts, inform = tf.main(input_text, input_number)
            excel(inform)
            wordcloudpic = wordcloud_texts(texts, 'fb')
            now = circular_graphic(texts)

            return render_template('/base/predict_fb.html', prediction_text=prediction['data'],
                                   wordcloud=wordcloudpic.decode('utf-8'), path_graph=now)


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
