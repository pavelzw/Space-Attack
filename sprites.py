# sprites.py
from user43_7yqHvQrReO_1 import Settings, Resources # properties.py
import random
from math import sqrt, cos, sin, pi

class Sprite:
    def __init__(self, type, pos=(0, 0), visible=False, rotation=0, scale=Settings.player_scale):
        self.type = type
        self.pos = pos
        self.image = Resources.images[self.type]
        self.size = self.image.get_width(), self.image.get_height()
        if self.size == (0, 0): # simplegui Bug, nicht vom Spiel
            print('SimpleGUI-Fehler')
        self.scale = scale
        self.rl_size = Settings.resolution[1] * scale * self.size[0] / self.size[1], Settings.resolution[1] * self.scale
        self.center = self.size[0] // 2, self.size[1] // 2
        self.visible = visible
        self.rotation = rotation

    def draw(self, canvas):
        if self.visible:
            canvas.draw_image(self.image, self.center,
                self.size, self.pos, self.rl_size, self.rotation)

    def update(self):
        pass

class Enemy(Sprite):
    def __init__(self, targets, enemy_names):
        Sprite.__init__(self, random.choice(enemy_names),
            visible=False, scale=Settings.enemy_scale)
        self.v = Settings.enemy_velocity
        self.targets = targets

    def spawn(self):
        self.visible = True
        edge = random.randint(0, 3)
        if edge == 0:  # linke Kante
            x = -self.rl_size[0]
            y = random.randint(int(-self.rl_size[1]), Settings.resolution[1])
        elif edge == 1:  # obere Kante
            x = random.randint(int(-self.rl_size[0]), Settings.resolution[0])
            y = -self.rl_size[1]
        elif edge == 2:  # rechte Kante
            x = Settings.resolution[0] + self.rl_size[0]
            y = random.randint(int(-self.rl_size[1]), Settings.resolution[1])
        elif edge == 3:  # untere Kante
            x = random.randint(int(-self.rl_size[0]), Settings.resolution[0])
            y = Settings.resolution[1] + self.rl_size[1]
        self.pos = x, y

    def update(self):
        self.move()

    def move(self):
        # Wurzel braucht man nicht
        min_dist = None
        min_dist_index = 0

        for index, target in enumerate(self.targets):
            if not target.alive:
                continue
            vec = target.pos[0] - self.pos[0], target.pos[1] - self.pos[1]
            dist = vec[0] * vec[0] + vec[1] * vec[1]
            if min_dist is None or dist < min_dist:
                min_dist = dist
                min_dist_index = index
        target = self.targets[min_dist_index].pos
        vec = target[0] - self.pos[0], target[1] - self.pos[1]
        vec_abs = sqrt(vec[0] * vec[0] + vec[1] * vec[1])
        vec = vec[0] / vec_abs, vec[1] / vec_abs
        self.pos = self.pos[0] + self.v * vec[0], self.pos[1] + self.v * vec[1]

class Laser(Sprite):
    def __init__(self, is_left, skin_name):
        Sprite.__init__(self, skin_name,
            visible=False, scale=Settings.laser_scale)
        self.rotation = 0
        self.is_left = is_left
        self.mov_vec = 0, 0

    def shoot(self, pos, rotation):
        self.visible = True
        self.rotation = rotation
        self.pos = pos
        self.mov_vec = cos(self.rotation - pi / 2), sin(self.rotation - pi / 2)

    def update(self):
        if self.visible:
            self.pos = (self.pos[0] + self.mov_vec[0] * Settings.laser_velocity,
                self.pos[1] + self.mov_vec[1] * Settings.laser_velocity)

    def is_valid(self):
        if self.pos[0] < 0 or self.pos[0] > Settings.resolution[0] or self.pos[1] < 1 or self.pos[1] > Settings.resolution[1]:
            return False
        return True

class PlayerSprite(Sprite):
    def __init__(self, player_number):
        Sprite.__init__(self, Settings.player2_skin if player_number else Settings.player1_skin,
            visible=True, scale=Settings.player_scale)
        self.num = player_number

class Player(PlayerSprite):
    left = 0
    right = 1
    def __init__(self, player_number, velocity=Settings.player_velocity, rot_speed=Settings.player_angular_velocity):
        PlayerSprite.__init__(self, player_number)
        self.v = velocity
        self.rot_speed = rot_speed
        self.is_turnleft = False
        self.is_turnright = False
        self.lasers = []
        self.max_cooldown = Settings.player_cooldown
        self.cooldown = 0
        self.score = 0
        self.invincible_counter = 0
        self.invincible_max = Settings.player_invulnerability_time
        self.laser_skin = Settings.player2_laser if player_number else Settings.player1_laser
        self.alive = True
        self.mov_vec = 0, 0
        if Settings.has_lifes:
            if Settings.modus == 'Hardmode':
                self.lifes = 1
            elif Settings.modus == 'Classic 10 Lifes':
                self.lifes = 10
            elif Settings.modus == 'Classic 5 Lifes':
                self.lifes = 5
            elif Settings.modus == 'Classic 3 Lifes':
                self.lifes = 3
            self.life_radius = min(Settings.resolution) / 80
            if not self.life_radius:
                self.life_radius = 1

    def turn(self, direction):
        if direction == Player.left:
            self.rotation -= self.rot_speed
        elif direction == Player.right:
            self.rotation += self.rot_speed

    def shoot(self):
        if not self.cooldown and self.alive:
            laser1, laser2 = Laser(True, self.laser_skin), Laser(False, self.laser_skin)
            n = -sin(self.rotation - pi / 2), cos(self.rotation - pi / 2)
            d = n[0] * Settings.laser_distance, n[1] * Settings.laser_distance
            laser1.shoot((self.pos[0] + d[0], self.pos[1] + d[1]), self.rotation)
            laser2.shoot((self.pos[0] - d[0], self.pos[1] - d[1]), self.rotation)
            self.lasers.append(laser1)
            self.lasers.append(laser2)
            self.cooldown = self.max_cooldown
            if Settings.sounds:
                Resources.sounds['Laser'].set_volume(.5)
                Resources.sounds['Laser'].play()

    def get_hit(self):
        if self.invincible_counter <= 0:
            if Settings.has_lifes:
                self.lifes -= 1
                if not self.lifes:
                    self.die()
            else:
                self.score = int(self.score * Settings.player_subtraction)
            self.invincible_counter = self.invincible_max

    def die(self):
        self.alive = False

    def update(self):
        if self.invincible_counter > 0:
            self.invincible_counter -= 1
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.is_turnleft or self.is_turnright:
            if self.is_turnright:
                self.turn(Player.right)
            else:
                self.turn(Player.left)
            self.mov_vec = cos(self.rotation - pi / 2) * self.v, sin(self.rotation - pi / 2) * self.v
        self.pos = self.pos[0] + self.mov_vec[0], self.pos[1] + self.mov_vec[1]
        self.lasers = [laser for laser in self.lasers if laser.is_valid()]

    def draw(self, canvas):
        if Settings.has_lifes:
            radius = self.life_radius
            if self.num:
                for life in range(self.lifes):
                    canvas.draw_circle((Settings.resolution[0] - (life + 1) * (radius + 5) * 2 - radius, 3 * radius), radius, 1, '#cdcdcd', Settings.blue)
            else:
                for life in range(self.lifes):
                    canvas.draw_circle(((life + 1) * (radius + 5) * 2 + radius, 3 * radius), radius, 1, '#cdcdcd', Settings.red)
        if self.alive:
            Sprite.draw(self, canvas)
            for laser in self.lasers:
                laser.draw(canvas)
