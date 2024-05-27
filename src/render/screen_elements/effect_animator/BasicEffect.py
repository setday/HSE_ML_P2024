class BasicEffect:
    def __init__(
            self,
            duration: float = 1,
            delay: float = 0,
            finish_callback=None,

            stay_after_finish: bool = False,
    ):
        """
        Basic effect

        @param duration: duration of the effect
        @param delay: delay before the effect starts
        @param finish_callback: callback when the effect is finished
        @param stay_after_finish: if True, effect will stay after finish
        """
        self.duration = duration
        self.delay = delay
        self.time_elapsed = 0
        self.finish_callback = finish_callback
        self.stay_after_finish = stay_after_finish

    def update(self, delta_time: float) -> None:
        if self.time_elapsed >= self.duration:
            self.time_elapsed = self.duration
            return
        if not self.is_started():
            self.delay -= delta_time
            return
        self.time_elapsed += delta_time

    def draw(self) -> None:
        pass

    def post_draw(self) -> None:
        self.draw()

    def is_finished(self) -> bool:
        return self.time_elapsed >= self.duration

    def is_started(self) -> bool:
        return self.delay <= 0

    def get_post_effect(self) -> "BasicEffect" or None:
        return self if self.stay_after_finish else None
