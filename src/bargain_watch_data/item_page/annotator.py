from dataclasses import dataclass, field
from typing import Dict, List

import ipywidgets as widgets
from IPython.display import display
from PIL.Image import Image

from bargain_watch_data.item_page import ItemPageController
from bargain_watch_data.item_page.consts import ItemImageStatus
from bargain_watch_data.item_page.models import ItemImage
from bargain_watch_data.item_page.utils import load_image, get_entropy_score


@dataclass
class ItemPageAnnotator:
    controller: ItemPageController
    _images_cache: Dict[str, Image] = field(default_factory=dict)

    def _load_images(self, images: List[ItemImage]):
        for image in images:
            if image.url not in self._images_cache:
                self._images_cache[image.url] = load_image(image.url)

    def reset(self):
        self._images_cache = {}

    def _get_sorted_images(self, images: List[ItemImage]):
        return sorted(
            images,
            key=lambda img: get_entropy_score(self._images_cache[img.url])
        )

    def draw(self):
        buttons_mapping = {}
        images = list(self.controller.item_page.images.values())
        self._load_images(images)

        def _on_button_clicked(arg):
            index = buttons_mapping[arg['owner']].index
            self.controller.set_image_status(index, ItemImageStatus(arg["new"]))

        def _draw_image(image: ItemImage):
            current_value = self.controller.get_image_status(image.index)
            button = widgets.ToggleButtons(
                value=current_value.name,
                options=[ItemImageStatus.ACCEPT.name, ItemImageStatus.REJECT.name],
                layout=widgets.Layout(width='auto'),
                style={"button_width": "auto"},
            )
            button.observe(_on_button_clicked, 'value')
            buttons_mapping[button] = image

            display(self._images_cache[image.url])
            display(button)

        for row in self._get_sorted_images(images):
            _draw_image(row)
