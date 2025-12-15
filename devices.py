import arcade


class Device(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.scale = 0.1
        self.center_x = x
        self.center_y = y
        self.is_hackable = True
        self.is_hacked = False
        self.interaction_distance = 50

    def can_interact(self, player_x, player_y):
        distance = ((self.center_x - player_x) ** 2 +
                    (self.center_y - player_y) ** 2) ** 0.5
        return distance < self.interaction_distance and self.is_hackable

    def hack(self):
        if not self.is_hacked:
            self.is_hacked = True  # сделать только в случае успеха
            self.is_hackable = False
            self.on_hack()
        else:
            pass

    def on_hack(self):
        pass


class Camera(Device):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.unhacked_texture = arcade.load_texture("images/devices/unhacked_camera.png")
        self.hacked_texture = arcade.load_texture("images/devices/hacked_camera.png")
        self.texture = self.unhacked_texture

    def on_hack(self):
        if self.hacked_texture:
            self.texture = self.hacked_texture
