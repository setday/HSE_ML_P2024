class BasicEffect:
    def __init__(self, duration: float = 1, delay: float = 0, finish_callback=None):
        self.duration = duration
        self.delay = delay
        self.time_elapsed = 0
        self.finish_callback = finish_callback

    def update(self, delta_time: float):
        if self.time_elapsed >= self.duration:
            self.time_elapsed = self.duration
            return
        if not self.is_started():
            self.delay -= delta_time
            return
        self.time_elapsed += delta_time

    def draw(self):
        pass

    def is_finished(self):
        return self.time_elapsed >= self.duration

    def is_started(self):
        return self.delay <= 0
