import typing

from arcade import Texture
from arcade.gui import UITextureButton, UIOnClickEvent


class UICheckButton(UITextureButton):
    """
    Button with two states, checked and unchecked

    @param x: x position
    @param y: y position
    @param width: width of the button
    @param height: height of the button
    @param textures_checked: textures for the checked state (normal, hovered, pressed)
    @param textures_unchecked: textures for the unchecked state (normal, hovered, pressed)
    @param scale: scale of the button
    @param style: style information for the button.
    @param on_change: callback, which is called, when the state changes
    @param checked: initial state of the button
    """

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = None,
        height: float = None,
        textures_checked: tuple[Texture, Texture, Texture] | None = None,
        textures_unchecked: tuple[Texture, Texture, Texture] | None = None,
        scale: float = None,
        style=None,
        on_change: typing.Callable or None = None,
        checked: bool = False,
        **kwargs
    ):
        if textures_checked is None:
            textures_checked = (None, None, None)
        if textures_unchecked is None:
            textures_unchecked = (None, None, None)

        self.textures_checked = textures_checked
        self.textures_unchecked = textures_unchecked
        self.checked = checked

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            texture=textures_checked[0] if checked else textures_unchecked[0],
            texture_hovered=textures_checked[1] if checked else textures_unchecked[1],
            texture_pressed=textures_checked[2] if checked else textures_unchecked[2],
            scale=scale,
            style=style,
            **kwargs
        )

        self.on_change = on_change

    def switch_state(self, state: bool):
        if self.checked == state:
            return

        self.checked = state

        self._tex = (
            self.textures_checked[0] if self.checked else self.textures_unchecked[0]
        )
        self._tex_hovered = (
            self.textures_checked[1] if self.checked else self.textures_unchecked[1]
        )
        self._tex_pressed = (
            self.textures_checked[2] if self.checked else self.textures_unchecked[2]
        )

    def on_click(self, event: UIOnClickEvent):
        self.switch_state(not self.checked)

        if self.on_change:
            self.on_change(self.checked)


def make_radio_from_check_buttons(
    buttons: list[UICheckButton], on_change: typing.Callable
):
    def unchecker(index: int) -> bool:
        if not buttons[index].checked:
            buttons[index].switch_state(True)
            return False
        for j, check_button in enumerate(buttons):
            check_button.switch_state(j == index)
        return True

    def create_lambda(index: int) -> typing.Callable:
        return lambda _: on_change(index) if unchecker(index) else None

    for i, button in enumerate(buttons):
        button.on_change = create_lambda(i)
        button.switch_state(False)
    buttons[0].switch_state(True)
