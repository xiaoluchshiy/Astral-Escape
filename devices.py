from math import degrees
from arcade.particles import FadeParticle, Emitter, EmitBurst, EmitInterval, EmitMaintainCount
from pyglet.graphics import Batch
import arcade
import random
from dataclasses import dataclass

SPARK_TEX = [
    arcade.make_soft_circle_texture(8, arcade.color.RED),
    arcade.make_soft_circle_texture(8, arcade.color.RED),
    arcade.make_soft_circle_texture(8, arcade.color.RED),
    arcade.make_soft_circle_texture(8, arcade.color.RED),
]
SMOKE_TEX = arcade.make_soft_circle_texture(20, arcade.color.LIGHT_GRAY, 255, 80)

def gravity_drag(p):  # Для искр: чуть вниз и затухание скорости
    p.change_y += -0.03
    p.change_x *= 0.92
    p.change_y *= 0.92


def smoke_mutator(p):  # Дым раздувается и плавно исчезает
    p.scale_x *= 1.02
    p.scale_y *= 1.02
    p.alpha = max(0, p.alpha - 2)

def make_smoke_puff(x, y):
    # Короткий «пых» дыма: медленно плывёт и распухает
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(12),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=SMOKE_TEX,
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 0.6),
            lifetime=random.uniform(1.5, 2.5),
            start_alpha=200, end_alpha=0,
            scale=random.uniform(0.6, 0.9),
            mutation_callback=smoke_mutator,
        ),
    )

def make_explosion(x, y, count=80):
    # Разовый взрыв с искрами во все стороны
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(count),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=random.choice(SPARK_TEX),
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 9.0),
            lifetime=random.uniform(0.5, 1.1),
            start_alpha=255, end_alpha=0,
            scale=random.uniform(0.35, 0.6),
            mutation_callback=gravity_drag,
        ),
    )

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
        self.unhacked_texture = arcade.load_texture("images/devices/camera_unhacked.png")
        self.hacked_texture = arcade.load_texture("images/devices/camera_hacked.png")
        self.radius = arcade.load_texture("images/devices/radius.png")
        self.texture = self.unhacked_texture
        self.change_angle = True
        self.rotation_speed = 20
        self.rotation_direction = 1
        self.max_angle = max_degrees
        self.angle = 0
        self.radius_angle = 0
        self.radius_rotation_speed = 20
        self.radius_direction = 1
        self.radius_size = 200
        self.emitters = []

    def on_hack(self):
        if self.hacked_texture:
            self.texture = self.hacked_texture
            self.emitters.append(make_explosion(self.center_x, self.center_y))
            self.emitters.append(make_smoke_puff(self.center_x, self.center_y))

    def update(self, delta_time):
        if not self.is_hacked and self.change_angle:
            self.angle += self.rotation_speed * delta_time * self.rotation_direction
            if abs(self.angle) >= self.max_angle:
                self.rotation_direction *= -1
            self.radius_angle += self.radius_rotation_speed * delta_time * self.radius_direction
            if self.radius_angle >= self.max_angle:
                self.radius_direction = -1
            elif self.radius_angle <= - self.max_angle:
                self.radius_direction = 1
            elif self.is_hacked:
                self.angle = 0
                self.radius_angle = 0
            emitters_copy = self.emitters.copy()  # Защищаемся от мутаций списка
            for e in emitters_copy:
                e.update(delta_time)
            for e in emitters_copy:
                if e.can_reap():  # Готов к уборке?
                    self.emitters.remove(e)

    def draw_radius(self):
        if not self.is_hacked:
            arcade.draw_arc_filled(
                self.center_x,
                self.center_y,
                self.radius_size * 2,
                self.radius_size * 2,
                (255, 0, 0, 100),
                self.radius_angle - (self.max_angle / 2),
                self.radius_angle + (self.max_angle / 2),
                32
            )
        else:
            pass


class Button(Device):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = arcade.load_texture('images/devices/button.png')
        self.scale = 0.07
        self.is_hackable = True

    def draw_radius(self):
        pass
