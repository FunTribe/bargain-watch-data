from dataclasses import dataclass, field
from typing import Dict, List

from bargain_watch_data.item_page.consts import ItemImageStatus


@dataclass
class ItemImage:
    index: int
    url: str
    status: ItemImageStatus = field(default=ItemImageStatus.REJECT)


@dataclass
class ItemPage:
    index: int
    url: str
    images: Dict[int, ItemImage] = field(default_factory=dict)

    @property
    def final_images(self) -> List[ItemImage]:
        return [
            image
            for image in self.images.values()
            if image.status != ItemImageStatus.REJECT
        ]
