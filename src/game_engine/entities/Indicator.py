import arcade


class Indicator:
    def __init__(
            self,
            owner,
            sprite_list,
            position=(300, 300),
            full_color: arcade.Color = arcade.color.GREEN,
            background_color: arcade.Color = arcade.color.BLACK,
            width: int = 100,
            height: int = 4,
            border_size: int = 4,
    ) -> None:

        self.owner = owner
        self.sprite_list = sprite_list

        self.box_width = width
        self.box_height = height
        self.half_box_width = self.box_width // 2
        self.center_x: float = 0.0
        self.center_y: float = 0.0
        self.fullness: float = 0.0

        self.background_box = arcade.SpriteSolidColor(
            self.box_width + border_size,
            self.box_height + border_size,
            background_color,
        )
        self.full_box = arcade.SpriteSolidColor(
            self.box_width,
            self.box_height,
            full_color,
        )
        self.sprite_list.add(self.background_box)
        self.sprite_list.add(self.full_box)

        self.fullness = 1.0
        self.position = position

    def set_fullness(self, new_fullness: float):
        self.fullness = new_fullness
        if new_fullness == 0.0:
            self.full_box.visible = False
        else:
            self.full_box.visible = True
            self.full_box.width = self.box_width * new_fullness
            self.full_box.left = self.center_x - (self.box_width // 2)

    def set_position(self, new_position) -> None:
        if new_position != self.position:
            self.center_x, self.center_y = new_position
            self.background_box.position = new_position
            self.full_box.position = new_position
            self.full_box.left = self.center_x - (self.box_width // 2)
