import arcade
from src.render.sprites.BasicSprite import BasicSprite


class ScoreDisplay:
    def __init__(self,
                 text,
                 start_x,
                 start_y,
                 color,
                 size,
                 width,
                 font_path,
                 font_name,
                 score,
                 coin="assets/coin.png"
                 ):
        if font_path is not None:
            arcade.load_font(font_path)
        self.current_score = self.target_score = score
        self.change_speed = 0.03
        self.text = arcade.Text(text, start_x, start_y, color, size, width, 'left', font_name=font_name)
        self.coin = BasicSprite(coin)

    def draw(self):
        self.text.draw()

    def set_position(self, new_position):
        self.text.position = new_position
        self.coin.center_x, self.coin.center_y = self.text.x - 50, self.text.y + 15

    def update_score(self, new_score):
        self.target_score = new_score
        self.current_score -= (self.current_score - self.target_score) * self.change_speed
        self.text.text = int(self.current_score)
