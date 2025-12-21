import arcade
from devices import Camera
import random
from alert import PressE

from pyglet.graphics import Batch

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Astral Escape"
PLAYER_SPEED = 200


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 0.1
        self.center_x = 0
        self.center_y = SCREEN_HEIGHT // 2
        self.change_x = 0
        self.change_y = 0
        self.texture = arcade.load_texture("images/player_back.png")
        self.texture_left = arcade.load_texture("images/player_left.png").flip_left_right()
        self.texture_right = arcade.load_texture("images/player_left.png")
        self.texture_back = arcade.load_texture("images/player_back.png")
        self.texture_forward = arcade.load_texture("images/player.png")
        self.astral_texture_left = arcade.load_texture("images/player_astral_left.png").flip_left_right()
        self.astral_texture_right = arcade.load_texture("images/player_astral_left.png")
        self.astral_texture_back = arcade.load_texture("images/player_astral_back.png")
        self.astral_texture_forward = arcade.load_texture("images/player_astral.png")
        self.astral_form = False
        self.astral_form_x = 0
        self.astral_form_y = 0

    def update(self, delta_time):
        self.center_x += self.change_x * PLAYER_SPEED * delta_time
        self.center_y += self.change_y * PLAYER_SPEED * delta_time

        # Ограничение движения в пределах экрана
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT


class Astral_Escape(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background = arcade.load_texture("images/prison.png")
        self.track_h = 2
        self.track_v = 2
        # устройства
        self.devices = None
        self.current_device = None
        self.world_camera = arcade.camera.Camera2D()

    def setup(self):
        # Создание объектов
        self.player = Player()
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        cam_alert = PressE(300, 350)
        self.alerts = arcade.SpriteList()
        self.alerts.append(cam_alert)
        self.devices = arcade.SpriteList()
        camera = Camera(300, 400, 45)
        self.devices.append(camera)
        self.change_form = arcade.SpriteList(self.player.texture_left)

    def on_draw(self):
        self.clear()
        # Отрисовка фона
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                                  SCREEN_WIDTH, SCREEN_HEIGHT)
                                 )
        if self.player.astral_form:
            arcade.draw_texture_rect(self.player.texture_right,
                                     arcade.rect.XYWH(self.player.astral_form_x, self.player.astral_form_y, 100,
                                                      100))
        if self.current_device:
            self.alerts.draw()
        self.player_list.draw()
        self.devices.draw()
        for device in self.devices:
            if not device.is_hacked:
                device.draw_radius()

        self.world_camera.use()

    def on_update(self, delta_time):

        if not self.player.astral_form:
            if self.track_h == 1:
                self.player.texture = self.player.texture_left
            if self.track_h == 0:
                self.player.texture = self.player.texture_right
            if self.track_v == 1:
                self.player.texture = self.player.texture_back
            if self.track_v == 0:
                self.player.texture = self.player.texture_forward
        else:
            if self.track_h == 1:
                self.player.texture = self.player.astral_texture_left
            if self.track_h == 0:
                self.player.texture = self.player.astral_texture_right

        self.player.update(delta_time)
        for device in self.devices:
            device.update(delta_time)
        self.current_device = None
        for device in self.devices:
            if device.can_interact(self.player.center_x, self.player.center_y):
                self.current_device = device
                break
        position = (self.player.center_x, self.player.center_y)
        self.world_camera.position = arcade.math.lerp_2d(self.world_camera.position, position, 0.12)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = 1
            self.track_v = 1
        elif key == arcade.key.S:
            self.player.change_y = -1
            self.track_v = 0
        elif key == arcade.key.A:
            self.player.change_x = -1
            self.track_h = 1
        elif key == arcade.key.D:
            self.player.change_x = 1
            self.track_h = 0
        elif key == arcade.key.Q:
            if self.player.astral_form:
                self.player.astral_form = False
                self.player.center_x = self.player.astral_form_x
                self.player.center_y = self.player.astral_form_y
                self.player.texture = self.player.texture_forward
            else:
                self.player.astral_form = True
                self.player.astral_form_x = self.player.center_x
                self.player.astral_form_y = self.player.center_y
                self.player.center_x = self.player.center_x + self.player.width
                self.player.texture = self.player.astral_texture_forward
        elif key == arcade.key.E:
            if self.current_device and not self.current_device.is_hacked:
                self.current_device.hack()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.player.change_y = 0
            self.track_v = 2
        elif key == arcade.key.A or key == arcade.key.D:
            self.player.change_x = 0
            self.track_h = 2


def setup_game(width=800, height=600, title="Red Hat collects berries"):
    game = Astral_Escape(width, height, title)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
