import arcade
import arcade.gui
import pyglet  # type: ignore[import-untyped]

PLAYERS: set = set()

MUSIC_MANAGER: list = []

VOLUME_LEVEL: float = 0.5


def get_sound_level() -> float:
    return VOLUME_LEVEL


def set_sound_level(volume: float) -> None:
    for player in PLAYERS:
        player.update_volume()

    for manager in MUSIC_MANAGER:
        manager.set_volume(volume)


def stop_all_players() -> None:
    global PLAYERS

    for player in PLAYERS:
        player.pause()


class MusicManager:
    def __init__(self, volume: float | None = None) -> None:
        self.track_list: list[str] = []
        self.track_index: int = 0

        self.volume: float = volume if volume is not None else get_sound_level()

        self.player: pyglet.media.Player | None = None

        self.cross_change_player: pyglet.media.Player | None = None
        self.cross_change_time: float = 0.0

        self.paused: bool = False

        MUSIC_MANAGER.append(self)

    def update(self, delta_time: float) -> None:
        if self.paused:
            return

        if self.player and not self.player.playing:
            self.next()

        if self.cross_change_time != 0.0:
            self.cross_change_time -= delta_time

            self.cross_change_time = max(0.0, self.cross_change_time)

            if self.player:
                self.player.volume = self.volume * (1 - self.cross_change_time)
            if self.cross_change_player:
                self.cross_change_player.volume = self.volume * self.cross_change_time

            if self.cross_change_time <= 0 and self.cross_change_player:
                self.cross_change_player.pause()
                self.cross_change_player = None

    def set_volume(self, volume: float | None = None) -> None:
        self.volume = volume if volume is not None else get_sound_level()

        if self.player:
            self.player.volume = self.volume * (1 - self.cross_change_time)
        if self.cross_change_player:
            self.cross_change_player.volume = self.volume * self.cross_change_time

    def change_track_list(self, track_list: list[str], loop: bool = False) -> None:
        self.track_list = track_list
        self.track_index = 0

        self.cross_change_player = self.player
        self.cross_change_time = 1.0

        self.player = None
        if self.track_list:
            self.player = arcade.Sound(
                self.track_list[self.track_index], streaming=True
            ).play(0.0, loop=loop)

    def next(self) -> None:
        if not self.track_list:
            return

        self.track_index = (self.track_index + 1) % len(self.track_list)

        self.cross_change_player = self.player
        self.cross_change_time = 1.0

        self.player = arcade.Sound(
            self.track_list[self.track_index], streaming=True
        ).play(0.0)

    def previous(self) -> None:
        if not self.track_list:
            return

        self.track_index = (len(self.track_list) + self.track_index - 1) % len(
            self.track_list
        )

        self.cross_change_player = self.player
        self.cross_change_time = 1.0

        self.player = arcade.Sound(
            self.track_list[self.track_index], streaming=True
        ).play(0.0)

    def play_pause(self) -> None:
        self.paused = not self.paused

        if self.paused:
            if self.player:
                self.player.pause()
            if self.cross_change_player:
                self.cross_change_player.pause()
        else:
            if self.player:
                self.player.play()
            if self.cross_change_player:
                self.cross_change_player.play()


class SoundPlayer:
    def __init__(self, path, volume: float | None = None, loop=False) -> None:
        global PLAYERS

        self.track = arcade.Sound(path, streaming=True)
        self.player = self.track.play(loop=loop)
        self.volume = volume if volume is not None else 1.0
        self.player.volume = self.volume * get_sound_level()
        self.player.play()

        PLAYERS.add(self)

    def __del__(self) -> None:
        global PLAYERS

        PLAYERS.remove(self)

    def pause(self):
        if self.player:
            self.player.pause()

    def resume(self):
        if self.player:
            self.player.play()

    def set_volume(self, volume) -> None:
        self.volume = volume
        self.update_volume()

    def update_volume(self) -> None:
        if self.player:
            self.player.volume = self.volume * get_sound_level()
