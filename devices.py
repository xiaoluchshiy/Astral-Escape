from math import degrees

import arcade


class Device(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.scale = 0.12
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
    def __init__(self, x, y, max_degrees):
        super().__init__(x, y)
        self.unhacked_texture = arcade.load_texture("images/devices/camera_unhacked.png").flip_left_right()
        self.hacked_texture = arcade.load_texture("images/devices/camera_hacked.png").flip_left_right()
        self.texture = self.unhacked_texture
        self.change_angle = True
        self.rotation_speed = 20
        self.rotation_direction = 1
        self.max_angle = max_degrees
        self.angle = 0

    def on_hack(self):
        if self.hacked_texture:
            self.texture = self.hacked_texture

    def update(self, delta_time):
        if not self.is_hacked and self.change_angle:
            self.angle += self.rotation_speed * delta_time * self.rotation_direction
            if abs(self.angle) >= self.max_angle:
                self.rotation_direction *= -1
        elif self.is_hacked:
            self.angle = 0