from dataclasses import dataclass

from bargain_watch_data.image_search.consts import ResultStatus
from bargain_watch_data.image_search.models import SearchResult
import ipywidgets as widgets
from IPython.display import Image, display, HTML

from bargain_watch_data.image_search.controller import SearchController


@dataclass
class SearchAnnotator:
    controller: SearchController

    def draw(self):
        buttons_mapping = {}

        def _on_button_clicked(arg):
            index = buttons_mapping[arg['owner']].index
            self.controller.set_result_status(index, ResultStatus(arg["new"]))

        def _draw_result(result: SearchResult):
            current_value = self.controller.get_result_status(result.index)
            img = Image(url=result.thumbnail_url)
            button = widgets.ToggleButtons(
                value=current_value.name,
                options=[ResultStatus.MATCH.name, ResultStatus.VARIANT.name, ResultStatus.REJECT.name],
                layout=widgets.Layout(width='auto'),
                style={"button_width": "auto"},
            )
            button.observe(_on_button_clicked, 'value')

            buttons_mapping[button] = result

            display(HTML(f"<h2>{result.title}</h2>"))
            display(HTML(f'<a href="{result.url}">{result.url}</span>'))
            display(img)
            display(button)

        for row in self.controller.results.values():
            _draw_result(row)
