import arcade


class Alert(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.scale = 0.35
        self.center_x = x
        self.center_y = y


class PressE(Alert):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = arcade.load_texture("images/devices/Press_E.png")
