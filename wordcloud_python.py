import matplotlib
matplotlib.use('Agg')
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random

size_x = 16 * 100
size_y = 7 * 100

def make_cloud(adjectives: dict):
    if not adjectives:
        return "NOPE"

    frequencies = {adj.capitalize(): count for adj, count in adjectives.items()}

    shared_config = dict(
        max_words=2000,
        width=size_x,
        height=size_y,
        min_font_size=2,
        stopwords=set(),
    )

    # Dark version
    mask_image = Image.open("images/github_green.png").resize((size_x, size_y))
    shared_config["mask"] = np.array(mask_image)
    wc = WordCloud(**shared_config, background_color="#1A1E2E")
    wc.generate_from_frequencies(frequencies)
    #wc.recolor(color_func=_color_dark)
    wc.to_file("static/images/cloud_dark.png")

    # Light version
    mask_image = Image.open("images/github_green.png").resize((size_x, size_y))
    shared_config["mask"] = np.array(mask_image)
    wc = WordCloud(**shared_config, background_color="#FAF7F2")
    wc.generate_from_frequencies(frequencies)
    #wc.recolor(color_func=_color_light)
    wc.to_file("static/images/cloud_light.png")
