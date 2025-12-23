import arcade
from devices import Camera, Button
import random
from alert import PressE

from pyglet.graphics import Batch

# Константы
SCREEN_WIDTH = 3000
SCREEN_HEIGHT = 1800
SCREEN_TITLE = "Astral Escape"
PLAYER_SPEED = 150
ANIMATION_SPEED = 0.085


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 0.08
        self.center_x = 690
        self.center_y = 720
        self.change_x = 0
        self.change_y = 0

        self.texture_right = arcade.load_texture("images/player/player_left1.png")
        self.texture_forward = arcade.load_texture("images/player/player_forward1.png")

        self.texture = arcade.load_texture("images/player/player_back1.png")

        self.textures_forward = []
        for i in range(3):
            texture = arcade.load_texture(f'images/player/player_forward{i}.png')
            self.textures_forward.append(texture)

        self.textures_back = []
        for i in range(3):
            texture = arcade.load_texture(f'images/player/player_back{i}.png')
            self.textures_back.append(texture)

        self.textures_left = []
        for i in range(3):
            texture = arcade.load_texture(f'images/player/player_left{i}.png')
            self.textures_left.append(texture)

        self.textures_right = []
        for i in range(3):
            texture = arcade.load_texture(f'images/player/player_left{i}.png').flip_left_right()
            self.textures_right.append(texture)

        self.astral_texture_left = arcade.load_texture("images/player/player_astral_left.png").flip_left_right()
        self.astral_texture_right = arcade.load_texture("images/player/player_astral_left.png")
        self.astral_texture_back = arcade.load_texture("images/player/player_astral_back.png")
        self.astral_texture_forward = arcade.load_texture("images/player/player_astral.png")

        self.astral_form = False
        self.astral_form_x = 0
        self.astral_form_y = 0

        self.is_walking = False

    def update(self, delta_time):
        old_x = self.center_x
        old_y = self.center_y
        if self.change_x != 0 and self.change_y != 0:
            self.center_x += self.change_x * PLAYER_SPEED // 2 * delta_time
            self.center_y += self.change_y * PLAYER_SPEED // 2 * delta_time
        else:
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

        self.is_walking = self.center_x != old_x or self.center_y != old_y

class Astral_Escape(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background = arcade.load_texture("images/space.png")
        self.track_h = 2
        self.track_v = 2
        self.door = True
        # устройства
        self.devices = None
        self.current_device = None
        self.world_camera = arcade.camera.Camera2D()

    def setup(self):
        # Создание объектов
        self.player = Player()
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.cam_alert = PressE(self.player.center_x, self.player.center_y - 30)
        self.alerts = arcade.SpriteList()
        self.alerts.append(self.cam_alert)
        self.devices = arcade.SpriteList()
        camera = Camera(570, 1220, 25)
        button = Button(1110, 809)
        self.devices.append(camera)
        self.devices.append(button)
        self.wall_list = arcade.SpriteList()
        map_name = "map/map.tmx"
        tile_map = arcade.load_tilemap(map_name, scaling=3)
        self.wall_list = tile_map.sprite_lists["walls"]
        self.door_list = tile_map.sprite_lists["door"]
        self.collision_list = tile_map.sprite_lists["collision"]
        self.astral_collision_list = tile_map.sprite_lists["astral_collision"]
        self.door_collision_list = tile_map.sprite_lists["door_collision"]
        self.astral_list = tile_map.sprite_lists["astral"]
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.collision_list)
        self.astral_physics_engine = arcade.PhysicsEngineSimple(self.player, self.astral_collision_list)
        self.door_physics_engine = arcade.PhysicsEngineSimple(self.player, self.door_collision_list)

        self.current_texture = 0
        self.texture_change_time = 0

    def update_animation(self, delta_time: float = 1 / 60):
        """ Обновление анимации """
        if not self.player.astral_form:
            if self.track_h == 1:
                if self.player.is_walking:
                    self.texture_change_time += delta_time
                    if self.texture_change_time >= ANIMATION_SPEED:
                        self.texture_change_time = 0
                        self.current_texture += 1
                        if self.current_texture >= len(self.player.textures_right):
                            self.current_texture = 0
                        self.player.texture = self.player.textures_right[self.current_texture]
            elif self.track_h == 0:
                if self.player.is_walking:
                    self.texture_change_time += delta_time
                    if self.texture_change_time >= ANIMATION_SPEED:
                        self.texture_change_time = 0
                        self.current_texture += 1
                        if self.current_texture >= len(self.player.textures_left):
                            self.current_texture = 0
                        self.player.texture = self.player.textures_left[self.current_texture]
            elif self.track_v == 1:
                if self.player.is_walking:
                    self.texture_change_time += delta_time
                    if self.texture_change_time >= ANIMATION_SPEED:
                        self.texture_change_time = 0
                        self.current_texture += 1
                        if self.current_texture >= len(self.player.textures_back):
                            self.current_texture = 0
                        self.player.texture = self.player.textures_back[self.current_texture]
            elif self.track_v == 0:
                if self.player.is_walking:
                    self.texture_change_time += delta_time
                    if self.texture_change_time >= ANIMATION_SPEED:
                        self.texture_change_time = 0
                        self.current_texture += 1
                        if self.current_texture >= len(self.player.textures_forward):
                            self.current_texture = 0
                        self.player.texture = self.player.textures_forward[self.current_texture]
            else:
                self.player.texture = self.player.texture_forward

    def on_draw(self):
        self.clear()
        # Отрисовка фона
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.wall_list.draw()
        if self.door:
            self.door_list.draw()
            self.door_collision_list.draw()
        if self.player.astral_form:
            arcade.draw_texture_rect(self.player.texture_right,
                                     arcade.rect.XYWH(self.player.astral_form_x, self.player.astral_form_y, 80,
                                                      80))
            self.astral_list.draw()
        self.player_list.draw()
        self.devices.draw()
        for device in self.devices:
            if not device.is_hacked:
                device.draw_radius()
        if self.current_device:
            self.alerts.draw()
        self.world_camera.use()

    def on_update(self, delta_time):
        self.cam_alert.center_y = self.player.center_y - 45
        self.cam_alert.center_x = self.player.center_x

        self.physics_engine.update()
        self.update_animation()
        if self.door:
            self.door_physics_engine.update()
        if not self.player.astral_form:
            self.astral_physics_engine.update()
        if  self.player.astral_form:
            if self.track_h == 1:
                self.player.texture = self.player.astral_texture_left
            if self.track_h == 0:
                self.player.texture = self.player.astral_texture_right
            if self.track_v == 1:
                self.player.texture = self.player.astral_texture_back
            if self.track_v == 0:
                self.player.texture = self.player.astral_texture_forward

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
                self.astral_physics_engine = arcade.PhysicsEngineSimple(self.player, self.astral_collision_list)
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


def setup_game(width=1200, height=800, title="Astral Escape"):
    game = Astral_Escape(width, height, title)
    game.setup()
    return game


def main():
    setup_game(1200, 800, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
