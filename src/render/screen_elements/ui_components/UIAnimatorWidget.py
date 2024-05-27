from arcade.gui import UIWidget

from src.render.screen_elements.ui_components.UISuperAnchorWidget import UISuperAnchorWidget


class UIAnimatableWidget(UISuperAnchorWidget):
    """
    Widget, which can be animated

    :param child: Child of this wrapper
    :param anchor_x: Which anchor to use for x axis (left, center, right)
    :param align_x: offset for x value (- = left, + = right)
    :param anchor_y: Which anchor to use for y axis (top, center, bottom)
    :param align_y: offset for y value (- = down, + = up)
    :param size_hint: Tuple of floats (0.0-1.0), how much space of the parent should be requested
    :param size_hint_min: min width and height in pixel
    :param size_hint_max: max width and height in pixel
    :param style: not used
    """

    def __init__(
        self, *, child: UIWidget, animator_type=None, animator_params=None, **kwargs
    ):
        self.delta_align_x = 0
        self.delta_align_y = 0

        super().__init__(child=child, **kwargs)

        if animator_type is None:
            self.animator = None
        else:
            self.animator = animator_type(self, **animator_params)

    @property
    def x(self):
        return super().x

    @x.setter
    def x(self, value):
        self.delta_align_x = value

    @property
    def y(self):
        return super().y

    @y.setter
    def y(self, value):
        self.delta_align_y = value

    def update_animation(self, delta_time: float):
        if self.animator is not None:
            self.animator.update(delta_time)

    def do_layout(self):
        self.align_x += self.delta_align_x
        self.align_y += self.delta_align_y

        super().do_layout()

        self.align_x -= self.delta_align_x
        self.align_y -= self.delta_align_y
