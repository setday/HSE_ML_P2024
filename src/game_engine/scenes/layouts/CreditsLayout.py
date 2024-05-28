from arcade.color import WHITE
from arcade.gui import UITextureButton, UIAnchorWidget, UIBoxLayout

from src.render.screen_elements.ui_components.UIFullScreenLayout import (
    UIFullScreenLayout,
)
from src.render.screen_elements.ui_components.UISuperText import UISuperText
from src.render.screen_elements.ui_components.UITexture import UITexture
from src.utils.Loaders import load_texture


class CreditsLayout(UIFullScreenLayout):
    def __init__(self, back_callback: callable):
        ###
        # Credits
        ###

        title = UIAnchorWidget(
            anchor_x="center",
            anchor_y="top",
            align_y=-10,
            child=UITexture(
                texture=load_texture("assets/pic/boards/Credits.png"),
                scale=7,
            ),
        )

        credits_texture = UITexture(
            texture=load_texture("assets/pic/extra/textured_plane.png"),
            scale=8,
        )
        credits_text = UIBoxLayout(
            space_between=20,
            children=[
                UISuperText(
                    text="CREDITS",
                    width=credits_texture.width - 100,
                    font_size=40,
                    align="center",
                    bold=True,
                ),
                UISuperText(
                    text="Alexander Serkov\n"
                    "-----------------------------------\n"
                    "|         Game Physics        |\n"
                    "=> |  Game Design / Visuals  | <=\n"
                    "| Concepts | Code design |\n"
                    "-----------------------------------",
                    width=credits_texture.width - 100,
                    multiline=True,
                    font_size=32,
                    align="center",
                    bold=True,
                ),
                UISuperText(
                    text="Artem Batygin\n"
                    "-----------------------------------\n"
                    "=> | Game AI | Game Interfaces | <=\n"
                    "-----------------------------------",
                    width=credits_texture.width - 100,
                    multiline=True,
                    font_size=32,
                    align="center",
                    bold=True,
                ),
                UISuperText(
                    text="Vladimir Zakharov\n"
                    "-----------------------------------\n"
                    "=> | Level design | Game AI | <=\n"
                    "-----------------------------------\n",
                    width=credits_texture.width - 100,
                    multiline=True,
                    font_size=32,
                    align="center",
                    bold=True,
                ),
                UISuperText(
                    text="Made with infinite ♥",
                    width=credits_texture.width - 100,
                    text_color=WHITE,
                    font_size=32,
                    align="center",
                ),
            ],
        )
        credits_texture.add(
            UIAnchorWidget(
                child=credits_text,
                anchor_x="center",
                anchor_y="top",
                align_y=-30,
            )
        )

        back_button = UITextureButton(
            texture=load_texture("assets/pic/buttons/Arrows/Right/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Arrows/Right/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Arrows/Right/pressed.png"),
            scale=7,
        )
        back_button.on_click = back_callback

        super().__init__(
            children=[
                UIAnchorWidget(
                    child=back_button,
                    anchor_x="right",
                    anchor_y="bottom",
                    align_y=75,
                    align_x=-75,
                ),
                UIAnchorWidget(child=credits_texture),
                title,
            ]
        )
