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
        self.target_health = 100
        self.current_health = 100
        self.box_width = width
        self.box_height = height
        self.half_box_width = self.box_width // 2
        self.center_x: float = 0.0
        self.center_y: float = 0.0

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
        self.middle_box = arcade.SpriteSolidColor(
            self.box_width,
            self.box_height,
            (255, 100, 0)
        )
        self.sprite_list.add(self.background_box)
        self.sprite_list.add(self.middle_box)
        self.sprite_list.add(self.full_box)
        self.change_speed = 1
        self.position = position

    def update_bar(self, new_health) -> None:
        self.target_health = max(0, new_health)
        self.current_health -= (self.current_health - self.target_health) * 0.03
        self.full_box.width = self.target_health
        self.middle_box.width = self.current_health
        self.middle_box.color = (255, 255, 0)

    def set_position(self, new_position) -> None:
        if new_position != self.position:
            self.center_x, self.center_y = new_position
            self.background_box.position = new_position
            self.full_box.position = new_position
            self.full_box.left = self.center_x - (self.box_width // 2)
            self.middle_box.position = new_position
            self.middle_box.left = self.center_x - (self.box_width // 2)
