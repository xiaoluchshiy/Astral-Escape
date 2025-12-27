from main import *
import arcade

class Player(arcade.Sprite):
    # создаем игрока
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
        # текстуры для ходьбы вперед
        for i in range(3):
            texture = arcade.load_texture(f'images/player/player_forward{i}.png')
            self.textures_forward.append(texture)

        self.textures_back = []
        # текстуры для ходьбы назад
        for i in range(3):
            texture = arcade.load_texture(f'images/player/player_back{i}.png')
            self.textures_back.append(texture)

        self.textures_left = []
        # для ходьбы влево
        for i in range(3):
            texture = arcade.load_texture(f'images/player/player_left{i}.png')
            self.textures_left.append(texture)

        self.textures_right = []
        # для ходьбы вправо
        for i in range(3):
            texture = arcade.load_texture(f'images/player/player_left{i}.png').flip_left_right()
            self.textures_right.append(texture)

        # астральная
        self.astral_texture_left = arcade.load_texture("images/player/player_astral_left.png").flip_left_right()
        self.astral_texture_right = arcade.load_texture("images/player/player_astral_left.png")
        self.astral_texture_back = arcade.load_texture("images/player/player_astral_back.png")
        self.astral_texture_forward = arcade.load_texture("images/player/player_astral.png")

        self.astral_form = False
        self.astral_form_x = 0
        self.astral_form_y = 0
        self.astral_timer = 0

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
