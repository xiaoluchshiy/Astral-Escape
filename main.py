import arcade
import random

from pyglet.graphics import Batch

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Astral Escape"
a = 1
PLAYER_SPEED = 200

BUSH_COUNT = 15
BUSH_SCALE = 0.4
BERRY_SCALE = 0.2


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 0.1
        self.center_x = 0
        self.center_y = SCREEN_HEIGHT // 2
        self.change_x = 0
        self.change_y = 0
        self.texture_left = arcade.load_texture("images/player.png")
        self.texture_right = arcade.load_texture("images/player.png").flip_left_right()

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

    def switch_form(self):
        self.astral_form = False
        pass


class Astral_Escape(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background = arcade.load_texture("images/prison.png")
        self.track = True

    def setup(self):
        # Создание объектов
        self.player = Player()
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

    def on_draw(self):
        self.clear()
        # Отрисовка фона
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                                  SCREEN_WIDTH, SCREEN_HEIGHT)
                                 )
        self.player_list.draw()

    def on_update(self, delta_time):
        if self.track:
            self.player.texture = self.player.texture_left
        else:
            self.player.texture = self.player.texture_right
        self.player.update(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = 1
        elif key == arcade.key.S:
            self.player.change_y = -1
        elif key == arcade.key.A:
            self.player.change_x = -1
            self.track = True
        elif key == arcade.key.D:
            self.player.change_x = 1
            self.track = False

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.player.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player.change_x = 0

def setup_game(width=800, height=600, title="Red Hat collects berries"):
    game = Astral_Escape(width, height, title)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
