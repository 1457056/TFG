#from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import base64
import matplotlib.pyplot as plt
from PIL import Image
import io
from os import remove
def wordcloud_texts(texts):
    """
    Metodo para crear el wordcloud
    :param texts:
    :return:
    """
    from wordcloud import WordCloud, ImageColorGenerator
    stopwords= (['AT_USER','https','RT']) + list(wordcloud.STOPWORDS())
    all_headlines = ' '.join(texts['Tweet'].str.lower())

    wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=1000).generate(all_headlines)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig('/home/gerard/Escritorio/TFG_deb/Webpage/static/images/wordcloud.jpg')

    im = Image.open('/home/gerard/Escritorio/TFG_deb/Webpage/static/images/wordcloud.jpg')
    data = io.BytesIO()
    im.save(data, "JPEG")

    # Then encode the saved image file.
    encoded_img_data = base64.b64encode(data.getvalue())
    return encoded_img_data


def circular_graphic(tweets):
    from wordcloud import WordCloud, ImageColorGenerator
    tweets['Label'].value_counts().plot(kind='pie', autopct='%.2f%%', title='Posts')

    plt.savefig('/home/gerard/Escritorio/TFG_deb/Webpage/static/images/circular_graph.jpg')

    im = Image.open('/home/gerard/Escritorio/TFG_deb/Webpage/static/images/circular_graph.jpg')
    data = io.BytesIO()
    im.save(data, "JPEG")

    # Then encode the saved image file.
    encoded_img_data_circular_graph = base64.b64encode(data.getvalue())
    return encoded_img_data_circular_graph
