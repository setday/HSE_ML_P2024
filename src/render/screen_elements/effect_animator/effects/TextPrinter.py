import arcade

from ..BasicEffect import BasicEffect


class TextPrinter(BasicEffect):
    def __init__(
        self,
        duration: float = 1,
        delay: float = 0,
        finish_callback=None,
        text_to_print: str = "",
        color: tuple[int, int, int] = arcade.color.WHITE,
        font_size: int = 100,
        appear: bool = True,
        text_object: arcade.Text | None = None,
        offset: tuple[int, int] = (0, 0),
        stay_after_finish: bool = False,
    ):
        """
        Fade effect

        @param duration: fade duration
        @param delay: delay before fade starts
        @param finish_callback: callback when fade is finished
        @param text_to_print: text to print
        @param appear: True = appear, False = disappear
        @param text_object: text object to print on
        @param stay_after_finish: if True, effect will stay after finish
        """

        super().__init__(duration, delay, finish_callback, stay_after_finish)

        self.alpha_multiplier = 255
        self.text_to_print = text_to_print
        self.appear = appear
        self.appear_progress = 0.0

        window_size = arcade.get_window().get_size()

        if text_object is None:
            text_object = arcade.Text(
                "",
                window_size[0] // 2 + offset[0],
                window_size[1] // 2 + offset[1],
                color,
                font_size,
                anchor_x="center",
                anchor_y="center",
                font_name="Karmatic Arcade",
            )
        self.text_object = text_object

    def update(self, delta_time: float) -> None:
        super().update(delta_time)

        self.appear_progress = self.time_elapsed / self.duration

        alpha = self.appear_progress
        if not self.appear:
            alpha = 1 - alpha
        letters_to_print = int(len(self.text_to_print) * alpha)

        self.text_object.text = self.text_to_print[:letters_to_print]

        window_size = arcade.get_window().get_size()
        self.text_object.center_x = window_size[0] // 2
        self.text_object.center_y = window_size[1] // 2

    def draw(self) -> None:
        self.text_object.draw()

    def is_finished(self) -> bool:
        return self.time_elapsed >= self.duration
