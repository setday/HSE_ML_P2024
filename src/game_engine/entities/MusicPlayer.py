import arcade
import arcade.gui


PLAYERS: set = set()


def update_all_players(volume: float) -> None:
    global PLAYERS

    for player in PLAYERS:
        player.set_volume(volume)


class MusicPlayer:
    def __init__(self, window: arcade.Window, volume: float) -> None:
        global PLAYERS

        self.window = window
        self.player = None
        self.volume = volume
        self.track_list = [
            "assets/sounds/Paul Mauriat - Minuetto.mp3",
            "assets/sounds/TheFatRat - Windfall.mp3",
            "assets/sounds/Piano Piano - It's My Life.mp3",
            "assets/sounds/Elektronomia - Sky High.mp3",
        ]
        self.track_index = 0

        self.track = arcade.Sound(self.track_list[self.track_index], streaming=True)

        self.ui_manager = arcade.gui.UIManager(self.window)
        box = arcade.gui.UIBoxLayout(vertical=False)

        ######################
        # Previous button
        ######################

        press_texture = arcade.load_texture(
            "assets/pic/buttons/Sound/prev_button_press.png"
        )
        normal_texture = arcade.load_texture(
            "assets/pic/buttons/Sound/prev_button_normal.png"
        )
        hover_texture = arcade.load_texture(
            "assets/pic/buttons/Sound/prev_button_hover.png"
        )

        self.right_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )

        self.right_button.on_click = self.previous  # type: ignoref
        self.right_button.scale(0.5)

        box.add(self.right_button)

        ######################
        # Backward button
        ######################

        press_texture = arcade.load_texture(
            "assets/pic/buttons/Sound/prev_button_press.png"
        )
        normal_texture = arcade.load_texture(
            "assets/pic/buttons/Sound/prev_button_normal.png"
        )
        hover_texture = arcade.load_texture(
            "assets/pic/buttons/Sound/prev_button_hover.png"
        )

        self.right_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )

        self.right_button.on_click = self.backward  # type: ignoref
        self.right_button.scale(0.5)

        box.add(self.right_button)

        ######################
        # Forward button
        ######################

        normal_texture = arcade.load_texture(
            "assets/pic/buttons/Sound/play_button_normal.png"
        )
        hover_texture = arcade.load_texture(
            "assets/pic/buttons/Sound/play_button_hover.png"
        )
        press_texture = arcade.load_texture(
            "assets/pic/buttons/Sound/play_button_press.png"
        )

        self.play_pause_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )

        self.play_pause_button.on_click = self.play_pause_button_clicked
        self.play_pause_button.scale(0.5)

        box.add(self.play_pause_button)

        ######################
        # Next button
        ######################

        press_texture = arcade.load_texture(
            "assets/pic/buttons/Sound/next_button_press.png"
        )
        normal_texture = arcade.load_texture(
            "assets/pic/buttons/Sound/next_button_normal.png"
        )
        hover_texture = arcade.load_texture(
            "assets/pic/buttons/Sound/next_button_hover.png"
        )

        self.right_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )

        self.right_button.on_click = self.forward  # type: ignore
        self.right_button.scale(0.5)

        box.add(self.right_button)

        ######################
        # Next button
        ######################

        press_texture = arcade.load_texture(
            "assets/pic/buttons/Sound/next_button_press.png"
        )
        normal_texture = arcade.load_texture(
            "assets/pic/buttons/Sound/next_button_normal.png"
        )
        hover_texture = arcade.load_texture(
            "assets/pic/buttons/Sound/next_button_hover.png"
        )

        self.right_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )

        self.right_button.on_click = self.next  # type: ignore
        self.right_button.scale(0.5)

        box.add(self.right_button)

        ######################
        # UI manager
        ######################

        # self.ui_manager.add(
        #     arcade.gui.UIAnchorWidget(child=box, anchor_x="left", anchor_y="bottom")
        # )
        self.ui_manager.enable()

        PLAYERS.add(self)

    def __del__(self) -> None:
        global PLAYERS

        PLAYERS.remove(self)

    def set_volume(self, volume: float) -> None:
        self.volume = volume
        if self.player:
            self.player.volume = self.volume

    def previous(self, *args) -> None:
        if self.player:
            self.track.stop(self.player)
            self.player.pop_handlers()
            self.player = None
        self.track_index = (len(self.track_list) + self.track_index - 1) % len(
            self.track_list
        )
        self.track = arcade.Sound(self.track_list[self.track_index], streaming=True)
        self.player = self.track.play()
        self.player.volume = self.volume
        self.player.push_handlers(on_eos=self.next)
        self.play_button()

    def next(self, *args) -> None:
        if self.player:
            self.track.stop(self.player)
            self.player.pop_handlers()
            self.player = None
        self.track_index = (self.track_index + 1) % len(self.track_list)
        self.track = arcade.Sound(self.track_list[self.track_index], streaming=True)
        self.player = self.track.play()
        self.player.volume = self.volume
        self.player.push_handlers(on_eos=self.next)
        self.play_button()

    def backward(self, *args) -> None:
        skip_time = 10

        if self.player:
            self.player.seek(max(0, self.player.time - skip_time))

    def forward(self, *args) -> None:
        skip_time = 10

        if self.player:
            self.player.seek(min(self.track.get_length(), self.player.time + skip_time))

    def play_button(self) -> None:
        self.play_pause_button.texture_pressed = arcade.load_texture(
            "assets/pic/buttons/Sound/pause_button_press.png"
        )
        self.play_pause_button.texture = arcade.load_texture(
            "assets/pic/buttons/Sound/pause_button_normal.png"
        )
        self.play_pause_button.texture_hovered = arcade.load_texture(
            "assets/pic/buttons/Sound/pause_button_hover.png"
        )

    def pause_button(self) -> None:
        self.play_pause_button.texture_pressed = arcade.load_texture(
            "assets/pic/buttons/Sound/play_button_press.png"
        )
        self.play_pause_button.texture = arcade.load_texture(
            "assets/pic/buttons/Sound/play_button_normal.png"
        )
        self.play_pause_button.texture_hovered = arcade.load_texture(
            "assets/pic/buttons/Sound/play_button_hover.png"
        )

    def play_pause_button_clicked(self, *args) -> None:
        if not self.player:
            self.player = self.track.play()
            self.player.volume = self.volume
            self.player.push_handlers(on_eos=self.next)
            self.play_button()
        elif not self.player.playing:
            self.player.volume = self.volume
            self.player.play()
            self.play_button()
        elif self.player.playing:
            self.player.pause()
            self.pause_button()

    def resume(self) -> None:
        if self.player and not self.player.playing:
            self.player.play()

    def pause(self) -> None:
        if self.player and self.player.playing:
            self.player.pause()

    def draw(self) -> None:
        self.ui_manager.draw()

        if self.player:
            arcade.draw_text(
                f"Time: {int(self.player.time // 60)}:{int(self.player.time % 60):02}",
                start_x=10,
                start_y=80,
                color=arcade.color.BLACK,
                font_size=24,
            )


class SoundPlayer:
    def __init__(self, path, volume, loop=False, ignore_update=False) -> None:
        global PLAYERS

        self.track = arcade.Sound(path, streaming=True)
        self.player = self.track.play(loop=loop)
        self.volume = volume
        self.ignore_update = ignore_update
        self.player.volume = self.volume
        self.player.play()

        PLAYERS.add(self)

    def __del__(self) -> None:
        global PLAYERS

        PLAYERS.remove(self)

    def pause(self):
        if self.player and self.player.playing:
            self.player.pause()

    def resume(self):
        if self.player and not self.player.playing:
            self.player.play()

    def set_volume(self, volume, update=True) -> None:
        self.volume = volume
        if self.player:
            if not update or not self.ignore_update:
                self.player.volume = self.volume
