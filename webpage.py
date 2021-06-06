import cv2
import numpy as np
import pandas
from PIL import Image
from flask import Flask, render_template, request, send_from_directory, current_app, send_file, make_response
import flask
import matplotlib
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import re
import prepare_out_texts as pot
from stop_words import get_stop_words
import pdfkit as pdfkit


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


def neg_color_func(word=None, font_size=None,
                   position=None, orientation=None,
                   font_path=None, random_state=None):
    """
    Color wordcloud
    :param word:
    :param font_size:
    :param position:
    :param orientation:
    :param font_path:
    :param random_state:
    :return:
    """
    h = 358
    s = 100  # 0 - 100
    l = random_state.randint(20, 70)  # 0 - 100
    return "hsl({}, {}%, {}%)".format(h, s, l)


def pos_color_func(word=None, font_size=None,
                   position=None, orientation=None,
                   font_path=None, random_state=None):
    """
        Color wordcloud
        :param word:
        :param font_size:
        :param position:
        :param orientation:
        :param font_path:
        :param random_state:
        :return:
        """
    h = 106
    s = 100  # 0 - 100
    l = random_state.randint(15, 70)  # 0 - 100
    return "hsl({}, {}%, {}%)".format(h, s, l)


def neu_color_func(word=None, font_size=None,
                   position=None, orientation=None,
                   font_path=None, random_state=None):
    """
        Color wordcloud
        :param word:
        :param font_size:
        :param position:
        :param orientation:
        :param font_path:
        :param random_state:
        :return:
        """
    h = 179
    s = 100  # 0 - 100
    l = random_state.randint(15, 70)  # 0 - 100
    return "hsl({}, {}%, {}%)".format(h, s, l)


def wordcloud_texts(texts, type, type_req_tw, word):
    """
    Metodo para crear el wordcloud
    Si es para Twitter se crea normal, con los tweets obtenidos
    Si es para facebook se recorren los comentarios de cada post, creando un wordcloud para cada uno de ellos
    :param texts:
    :return:
    """

    word = re.sub(r'\#','',word)
    stopwords = (['AT_USER', 'https', 'RT', 'de', 'la', 'con', 'por', 'en', 'una', 'que', 'q', 'y', 'el', 'lo', 'se',
                  'a', 'un', 't', 'co', 'así', 'què', 'mes', 'més', 'perque', 'són', 'fet',
                  'lis', '<', '>', '=','v','gt',word] + stop_words_sp + stopw_sp + stop_words_en + stop_words_ca + stop_words_spa)

    plt.figure(figsize=(50, 40))
    mask_neg = np.array(Image.open(r'D:\UAB\Uni\TFG\def_TFG\static\images\masks\mask_neg.png'))
    mask_neu = np.array(Image.open(r'D:\UAB\Uni\TFG\def_TFG\static\images\masks\mask_neu.png'))
    mask_pos = np.array(Image.open(r'D:\UAB\Uni\TFG\def_TFG\static\images\masks\mask_pos.png'))

    if type == 'tw':
        if type_req_tw != 'user':

            neg_headlines_tw = texts['Tweet'][texts['Rate'] < -0.5]
            filter_neg_headlines_tw = texts['Tweet'][texts['Rate'] < -0.5].index
            texts = texts.drop(filter_neg_headlines_tw)

            pos_headlines_tw = texts['Tweet'][texts['Rate'] > 0.5]
            filtre_pos_headlines_tw = texts['Tweet'][texts['Rate'] > 0.5].index
            texts = texts.drop(filtre_pos_headlines_tw)

            neu_headlines_tw = texts['Tweet']

            neg_headlines_tw = ' '.join(neg_headlines_tw.str.lower())
            pos_headlines_tw = ' '.join(pos_headlines_tw.str.lower())
            neu_headlines_tw = ' '.join(neu_headlines_tw.str.lower())

            # NEGATIVE WC
            wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=100,
                                  color_func=neg_color_func, width=600, height=403, contour_color='black',
                                  mask=mask_neg).generate(neg_headlines_tw)
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.savefig(r'D:\UAB\Uni\TFG\def_TFG\static\images\tw_images\neg_wordcloud.jpg', bbox_inches='tight')

            # POSITIVE WC
            wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=100,
                                  color_func=pos_color_func, width=600, height=403, contour_color='black',
                                  mask=mask_pos).generate(pos_headlines_tw)
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.savefig(r'D:\UAB\Uni\TFG\def_TFG\static\images\tw_images\pos_wordcloud.jpg', bbox_inches='tight')

            # NEUTRAL WC
            wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=100,
                                  color_func=neu_color_func, width=600, height=403, contour_color='black',
                                  mask=mask_neu).generate(neu_headlines_tw)
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.savefig(r'D:\UAB\Uni\TFG\def_TFG\static\images\tw_images\neu_wordcloud.jpg', bbox_inches='tight')

            # CONCATENATE IMAGES
            im1 = cv2.imread(r'D:\UAB\Uni\TFG\def_TFG\static\images\tw_images\neg_wordcloud.jpg')
            im2 = cv2.imread(r'D:\UAB\Uni\TFG\def_TFG\static\images\tw_images\neu_wordcloud.jpg')
            im3 = cv2.imread(r'D:\UAB\Uni\TFG\def_TFG\static\images\tw_images\pos_wordcloud.jpg')

            imh_h = cv2.hconcat([im1, im2, im3], None)
            cv2.imwrite(r'D:\UAB\Uni\TFG\def_TFG\static\images\tw_images\wordcloud.jpg', imh_h)



        else:
            texts.sort_values('Date')
            plt.figure()
            data = texts['Date'].value_counts()
            data = data.sort_index()
            data = data.iloc[0:5]
            plt.bar(data.index, data)
            plt.xticks(rotation=45)
            plt.subplots_adjust(bottom=0.2, top=0.98)
            plt.xlabel('Dia')
            plt.ylabel('Numero de Tweets')
            plt.savefig(r'D:\UAB\Uni\TFG\def_TFG\static\images\tw_images\wordcloud.jpg')

    else:
        filter_comments = pandas.DataFrame(columns=['Comments', 'Comments rate'])

        # Prepare data

        index_texts = texts
        index_texts = pot.top_texts(index_texts)
        texts = texts.sort_values('Rate')
        texts.reset_index(level=0, inplace=True)
        index_texts.reset_index(level=0, inplace=True)

        for index, id in enumerate(index_texts['Id']):
            id = index_texts['Id'][index]

            # De cada index que sea igual que los 4 psots que se mostrarán cogemos comentarios y rating

            for index2, i in enumerate(texts.index):
                if id == texts['Id'][index2]:
                    filter_comments = filter_comments.append({
                        'Comments': texts['Comments'][index2],
                        'Comments rate': texts['Comments rate'][index2]
                    }, ignore_index=True)

            filter_comments = filter_comments.iloc[0:-1]

            # SI no hay suficientes comentarios mostramos NOT ENOUGH DATA
            if len(filter_comments['Comments']) <= 7:
                output_name = r'D:\UAB\Uni\TFG\def_TFG\static\images\fb_images\wordclouds\wordcloud' + str(
                    index) + '.jpg'
                img_src = cv2.imread(r'D:\UAB\Uni\TFG\def_TFG\static\images\not_data.png')

                cv2.imwrite(output_name, img_src)
                filter_comments = filter_comments.iloc[0:0]

            else:

                neg_headlines_tw = filter_comments['Comments'][filter_comments['Comments rate'] < -0.5]
                filter_neg_headlines_tw = filter_comments['Comments'][filter_comments['Comments rate'] < -0.5].index
                filter_comments = filter_comments.drop(filter_neg_headlines_tw)

                pos_headlines_tw = filter_comments['Comments'][filter_comments['Comments rate'] > 0.5]
                filtre_pos_headlines_tw = filter_comments['Comments'][filter_comments['Comments rate'] > 0.5].index
                filter_comments = filter_comments.drop(filtre_pos_headlines_tw)

                neu_headlines_tw = filter_comments['Comments']

                # Preparamos datos para WC
                neg_headlines_tw = neg_headlines_tw.str.cat(sep=' ')
                pos_headlines_tw = pos_headlines_tw.str.cat(sep=' ')
                neu_headlines_tw = neu_headlines_tw.str.cat(sep=' ')

                # NEGATIVE WC
                wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=100,
                                      color_func=neg_color_func, width=600, height=403, contour_color='black',
                                      mask=mask_neg).generate(neg_headlines_tw)
                plt.imshow(wordcloud)
                plt.axis("off")
                plt.tight_layout(pad=0)
                plt.savefig(r'D:\UAB\Uni\TFG\def_TFG\static\images\fb_images\wordclouds\neg_wordcloud' + str(
                    index) + '.jpg', bbox_inches='tight')

                # POSITIVE WC
                wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=100,
                                      color_func=pos_color_func, width=600, height=403, contour_color='black',
                                      mask=mask_pos).generate(pos_headlines_tw)
                plt.imshow(wordcloud)
                plt.axis("off")
                plt.tight_layout(pad=0)
                plt.savefig(r'D:\UAB\Uni\TFG\def_TFG\static\images\fb_images\wordclouds\pos_wordcloud' + str(
                    index) + '.jpg', bbox_inches='tight')

                # NEUTRAL WC
                wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=100,
                                      color_func=neu_color_func, width=600, height=403, contour_color='black',
                                      mask=mask_neu).generate(neu_headlines_tw)
                plt.imshow(wordcloud)
                plt.axis("off")
                plt.tight_layout(pad=0)
                plt.savefig(r'D:\UAB\Uni\TFG\def_TFG\static\images\fb_images\wordclouds\neu_wordcloud' + str(
                    index) + '.jpg', bbox_inches='tight')

                # CONCATENATE IMAGES
                im1 = cv2.imread(r'D:\UAB\Uni\TFG\def_TFG\static\images\fb_images\wordclouds\neg_wordcloud' + str(
                    index) + '.jpg')
                im2 = cv2.imread(r'D:\UAB\Uni\TFG\def_TFG\static\images\fb_images\wordclouds\neu_wordcloud' + str(
                    index) + '.jpg')
                im3 = cv2.imread(r'D:\UAB\Uni\TFG\def_TFG\static\images\fb_images\wordclouds\pos_wordcloud' + str(
                    index) + '.jpg')

                imh_h = cv2.hconcat([im1, im2, im3], None)
                cv2.imwrite(r'D:\UAB\Uni\TFG\def_TFG\static\images\fb_images\wordclouds\wordcloud' + str(
                    index) + '.jpg', imh_h)
                filter_comments = filter_comments.iloc[0:0]


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
                    index) + '.png'
                img_src = cv2.imread(r'D:\UAB\Uni\TFG\def_TFG\static\images\nocomments.png')

                cv2.imwrite(output_name, img_src)

            else:
                plt.figure()
                plt.pie(data, colors=colors, labels=labels, shadow=True, autopct='%.2f%%')
                plt.legend(loc="best")
                plt.axis('equal')
                plt.savefig(
                    r'D:\UAB\Uni\TFG\def_TFG\static\images\fb_images\graphics\circular_graph' + str(index) + '.png',
                    transparent=False)

            del data
            del labels


def excel(dframe):
    """
    Metodo que crea un excel con el análisis para descargarlo posteriormente
    @param dframe:
    @param type:
    """
    dframe.to_excel(r'D:\UAB\Uni\TFG\def_TFG\Result_df\informe.xlsx')


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

            prediction, texts, type_req = tt.main(input_text, input_number, input_date_start, input_date_end)

            texts = texts.drop(['Comments', 'Comments label', 'Comments rate', 'Neg_com', 'Neu_com', 'Pos_com'], axis=1)
            excel(texts)
            wordcloud_texts(texts, 'tw', type_req, input_text)
            circular_graphic(texts, 'tw')

            if 'PDF' in request.form:
                template = 'child/table_tw.html'
                pdf = 'PDF'
            else:
                template = 'child/cards_tw.html'
                pdf = ''

            return render_template(template, prediction_text=prediction['data'], type=type_req, pdf=pdf)


        elif 'facebook' in request.form:
            from Facebook import test_fb_posts as tf

            if 'number' in request.form:
                input_number = int(request.form['number'])

            prediction, texts = tf.main(input_text, input_number)
            texts = texts.drop(['Date'], axis=1)
            excel(texts)
            wordcloud_texts(texts, 'fb', None, input_text)
            circular_graphic(texts, 'fb')

            return render_template('/predict_fb.html', prediction_text=prediction['data'])


@app.route('/download_info')
def downloadFile():
    """
    Método para descargar excel con análisis
    @return:
    """
    path = "Result_df/df_postss.xlsx"
    return send_file(path, as_attachment=True)


@app.route('/download_pdf')
def downloadPDF():
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    options = {'enable-local-file-access': None}

    css = r'D:\UAB\Uni\TFG\def_TFG\static\css\style.css'
    rendered = render_template('predict_fb.html')
    pdf = pdfkit.from_string(rendered, False, configuration=config, options=options, css=css)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response


if __name__ == "__main__":
    app.run(debug=True)
