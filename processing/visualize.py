import pandas as pd
import wordcloud
import matplotlib.pyplot as plt

plt.style.use("fivethirtyeight")


def word_cloud_image(df, column_name, image_name="wordcloud.png"):

    """
    function that creates WordCloud image based on input dataframe column

    :df: dataframe \n
    :column_name: column to convert to wrod clood \n
    :image_name: path where to save image, for ex "data/wordcloud.png" \n
    """
    words = " ".join([twts for twts in df[column_name]])
    cloud = wordcloud.WordCloud(
        width=500, height=300, random_state=21, max_font_size=110
    ).generate(words)
    plt.imshow(cloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(image_name)
