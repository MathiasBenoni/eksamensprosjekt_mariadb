import matplotlib
matplotlib.use('Agg')
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random

size_x = 400
size_y = 400

# Light mode: darker teal shades visible on warm off-white #FAF7F2
def _color_light(word, font_size, position, orientation, random_state=None, **kwargs):
    h = random.randint(172, 185)
    s = random.randint(42, 58)
    l = random.randint(30, 48)
    return f"hsl({h},{s}%,{l}%)"

# Dark mode: brighter teal shades visible on deep navy #1A1E2E
def _color_dark(word, font_size, position, orientation, random_state=None, **kwargs):
    h = random.randint(172, 185)
    s = random.randint(48, 65)
    l = random.randint(52, 70)
    return f"hsl({h},{s}%,{l}%)"

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
    wc.recolor(color_func=_color_dark)
    wc.to_file("static/images/cloud_dark.png")

    # Light version
    mask_image = Image.open("images/github_green.png").resize((size_x, size_y))
    shared_config["mask"] = np.array(mask_image)
    wc = WordCloud(**shared_config, background_color="#FAF7F2")
    wc.generate_from_frequencies(frequencies)
    wc.recolor(color_func=_color_light)
    wc.to_file("static/images/cloud_light.png")
