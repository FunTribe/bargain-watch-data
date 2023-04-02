from io import BytesIO

import requests
from PIL import Image
from scipy.stats import entropy


def load_image(url: str) -> Image:
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def get_entropy_score(img: Image):
    return entropy(img.histogram())
