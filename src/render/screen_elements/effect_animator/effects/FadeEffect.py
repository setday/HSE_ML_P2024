import arcade

from src.render.screen_elements.effect_animator.BasicEffect import BasicEffect


class FadeEffect(BasicEffect):
    def __init__(
            self,
            duration: float = 1,
            delay: float = 0,
            finish_callback=None,

            fade_color: tuple[int, int, int] = (0, 0, 0),
            fade_in: bool = True,
    ):
        """
        Fade effect

        @param duration: fade duration
        @param delay: delay before fade starts
        @param finish_callback: callback when fade is finished
        @param fade_color: color to fade to
        @param fade_in: True = fade in, False = fade out
        """

        super().__init__(duration, delay, finish_callback)

        self.fade_color = fade_color
        self.fade_in = fade_in
        self.fade_progress = 0

    def update(self, delta_time: float):
        super().update(delta_time)

        self.fade_progress = self.time_elapsed / self.duration

    def draw(self):
        alpha = self.fade_progress
        if not self.fade_in:
            alpha = 1 - alpha
        arcade.draw_xywh_rectangle_filled(
            0,
            0,
            arcade.get_window().width,
            arcade.get_window().height,
            color=(*self.fade_color, alpha * 255),
        )

    def is_finished(self):
        return self.time_elapsed >= self.duration
