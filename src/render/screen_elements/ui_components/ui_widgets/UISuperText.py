import arcade
import pyglet  # type: ignore[import-untyped]
from arcade.gui import UILabel


class UISuperText(UILabel):
    """A simple text label. Also supports multiline text.
    In case you want to scroll text use a :class:`UITextArea`
    By default a :class:`UILabel` will fit its initial content,
    if the text changed use :meth:`UILabel.fit_content` to adjust the size.

    :param float x: x coordinate of bottom left
    :param float y: y coordinate of bottom left
    :param float width: width of widget. Defaults to text width if not specified.
    :param float height: height of widget. Defaults to text height if not specified.
    :param str text: text of the label.
    :param font_name: a list of fonts to use. Program will start at the beginning of the list
                      and keep trying to load fonts until success.
    :param float font_size: size of font.
    :param arcade.Color text_color: Color of font.
    :param bool bold: Bold font style.
    :param bool italic: Italic font style.
    :param bool stretch: Stretch font style.
    :param str anchor_x: Anchor point of the X coordinate: one of ``"left"``,
                         ``"center"`` or ``"right"``.
    :param str anchor_y: Anchor point of the Y coordinate: one of ``"bottom"``,
                         ``"baseline"``, ``"center"`` or ``"top"``.
    :param str align: Horizontal alignment of text on a line, only applies if a width is supplied.
                      One of ``"left"``, ``"center"`` or ``"right"``.
    :param float dpi: Resolution of the fonts in this layout.  Defaults to 96.
    :param bool multiline: if multiline is true, a \\n will start a new line.
                           A UITextWidget with multiline of true is the same thing as UITextArea.

    :param size_hint: Tuple of floats (0.0-1.0), how much space of the parent should be requested
    :param size_hint_min: min width and height in pixel
    :param size_hint_max: max width and height in pixel
    :param style: Not used.
    """

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float | None = None,
        height: float | None = None,
        text: str = "",
        font_name=("Arial",),
        font_size: float = 12,
        text_color: arcade.Color = (255, 255, 255, 255),
        bold=False,
        italic=False,
        stretch=False,
        anchor_x="left",
        anchor_y="bottom",
        align="left",
        dpi=None,
        multiline: bool = False,
        size_hint=None,
        size_hint_min=None,
        size_hint_max=None,
        style=None,
        **kwargs
    ):
        super().__init__(
            x,
            y,
            width,
            height,
            text,
            font_name,
            font_size,
            text_color,
            bold,
            italic,
            stretch,
            anchor_x,
            anchor_y,
            align,
            dpi,
            False,
            size_hint,
            size_hint_min,
            size_hint_max,
            style,
            **kwargs
        )
        self.label = pyglet.text.Label(
            text=text,
            font_name=font_name,
            font_size=font_size,
            color=arcade.get_four_byte_color(text_color),
            width=width,
            height=height,
            bold=bold,
            italic=italic,
            stretch=stretch,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            align=align,
            dpi=dpi,
            multiline=multiline,
        )

        self._rect = self._rect.resize(height=self.label.content_height)
