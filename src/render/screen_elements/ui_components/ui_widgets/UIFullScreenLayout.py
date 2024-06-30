from typing import List

import arcade
from arcade.gui import UIWidget, UILayout


class UIFullScreenLayout(UILayout):
    """
    Layout, which fills the whole screen

    :param children: List of children
    :param style: not used
    """

    def __init__(self, children: List[UIWidget], style: dict | None = None):
        window = arcade.get_window()
        super().__init__(
            x=0,
            y=0,
            width=window.width,
            height=window.height,
            children=children,
            style=style,
        )

    def do_layout(self):
        window = arcade.get_window()
        self.rect = self.rect.resize(window.width, window.height)
        super().do_layout()
