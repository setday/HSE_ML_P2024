import arcade
from arcade.gui import UIWidget, UIAnchorWidget


class UISuperAnchorWidget(UIAnchorWidget):
    """
    UIAnchorWidget, which can have relative alignment to the parent widget

    :param child: Child of this wrapper
    :param relative_x: If True, align_x are relative to the parent widget
    :param relative_y: If True, align_y are relative to the parent widget

    :param anchor_x: Which anchor to use for x-axis (left, center, right)
    :param align_x: offset for x value (- = left, + = right)
    :param anchor_y: Which anchor to use for y-axis (top, center, bottom)
    :param align_y: offset for y value (- = down, + = up)
    :param size_hint: Tuple of floats (0.0-1.0), how much space of the parent should be requested
    :param size_hint_min: min width and height in pixel
    :param size_hint_max: max width and height in pixel
    :param style: not used
    """

    def __init__(self, *, child: UIWidget, relative_x: bool = False, relative_y: bool = False, **kwargs):
        self.relative_x = relative_x
        self.relative_y = relative_y

        super().__init__(child=child, **kwargs)

    def do_layout(self):
        super().do_layout()
        relative_align_x = self.align_x
        relative_align_y = self.align_y

        rect = self.rect
        rect_copy = self.rect.resize(0, 0).align_center(0, 0)
        parent_rect = self.parent.rect if self.parent else rect_copy.resize(*arcade.get_window().get_size())

        anchor_x = "center_x" if self.anchor_x == "center" else self.anchor_x
        own_anchor_x_value = getattr(rect, anchor_x)
        par_anchor_x_value = getattr(parent_rect, anchor_x)
        if self.relative_x:
            relative_align_x *= parent_rect.width
        diff_x = par_anchor_x_value + relative_align_x - own_anchor_x_value

        anchor_y = "center_y" if self.anchor_y == "center" else self.anchor_y
        own_anchor_y_value = getattr(rect, anchor_y)
        par_anchor_y_value = getattr(parent_rect, anchor_y)
        if self.relative_y:
            relative_align_y *= parent_rect.height
        diff_y = par_anchor_y_value + relative_align_y - own_anchor_y_value

        if diff_x or diff_y:
            self.rect = self.rect.move(diff_x, diff_y)
