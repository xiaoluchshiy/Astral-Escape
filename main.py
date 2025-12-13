import arcade
import random

from pyglet.graphics import Batch

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Red Hat collects berries"

GIRL_SCALE = 0.5
GIRL_SPEED = 200

BUSH_COUNT = 15
BUSH_SCALE = 0.4
BERRY_SCALE = 0.2


class Girl(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("images/player.png")
        self.scale = 0.05
        self.center_x = 0
        self.center_y = SCREEN_HEIGHT // 2
        self.change_x = 0
        self.change_y = 0

    def update(self, delta_time):
        self.center_x += self.change_x * GIRL_SPEED * delta_time
        self.center_y += self.change_y * GIRL_SPEED * delta_time

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

    def setup(self):
        # Создание объектов
        self.girl = Girl()
        self.girl_list = arcade.SpriteList()
        self.girl_list.append(self.girl)
        self.bushes = arcade.SpriteList()
        self.berries = arcade.SpriteList()
        self.batch = Batch()
        self.score = 0

    def on_draw(self):
        self.clear()
        # Отрисовка фона
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                                  SCREEN_WIDTH, SCREEN_HEIGHT)
                                 )

        # Отрисовка объектов
        self.bushes.draw()
        self.berries.draw()
        self.girl_list.draw()

        # Отрисовка счета
        arcade.draw_text(
            f"Ягод: {self.score}", SCREEN_WIDTH - 200,30, arcade.color.RED, 18)

    def on_update(self, delta_time):
        self.girl.update(delta_time)

        # Проверка сбора ягод
        collected_berries = arcade.check_for_collision_with_list(self.girl, self.berries)
        for berry in collected_berries:
            berry.remove_from_sprite_lists()
            self.score += 1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.girl.change_y = 1
        elif key == arcade.key.S:
            self.girl.change_y = -1
        elif key == arcade.key.A:
            self.girl.change_x = -1
        elif key == arcade.key.D:
            self.girl.change_x = 1

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.girl.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.girl.change_x = 0


def setup_game(width=800, height=600, title="Red Hat collects berries"):
    game = Astral_Escape(width, height, title)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
