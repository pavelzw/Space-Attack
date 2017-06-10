from math import pi, sin, cos, sqrt, exp
import random
import simplegui

class Settings:
    resolution = 1152, 648 # 3/5 von Full HD
    player_velocity = 1.5
    player_angular_velocity = pi / 180 # Geschwindigkeit, mit der sich Spieler dreht
    player_scale = .1
    player_cooldown = 50
    player_invulnerability_time = 450
    player_subtraction = 0.75
    enemy_scale = .1
    enemy_velocity = .5
    laser_scale = .03
    laser_velocity = 6
    laser_distance = resolution[1] * player_scale * .4
    wraparound = True  # rechts raus, links wieder rein
    growth_max_limit = 1000
    growth_min_limit = 200
    growth_const = 0.06
    player1_laser = 'Laser1'
    player2_laser = 'Laser1'
    player1_skin = 'Player1'
    player2_skin = 'Player1'

class Resources:
    image_urls = {
        'Background1' : 'http://i.imgur.com/q6ivRR9.png',
        'Background2' : 'http://i.imgur.com/x9DaE82.png',

        'Alien' : 'http://i.imgur.com/KdPWXXD.png',
        'Batman' : 'http://i.imgur.com/U8H5uo0.png',
        'Superman' : 'http://i.imgur.com/uHOwtoy.png',
        'Android' : 'http://i.imgur.com/J8l8oIC.png',
        'Ironman' : 'http://i.imgur.com/Lv5o6sh.png',
        'Spiderman' : 'http://i.imgur.com/ZO2iYfG.png',
        'Mario' : 'http://i.imgur.com/8HFD1Qp.png',
        'Ninja' : 'http://i.imgur.com/VWT66Bs.png',
        'Darth Vader' : 'http://i.imgur.com/JKXhtFA.png',
        'Stormtrooper' : 'http://i.imgur.com/dfBvqyx.png',
        'Donald Duck' : 'http://i.imgur.com/xSLMyYh.png',
        'Mickey Mouse' : 'http://i.imgur.com/jOOJ6IB.png',
        'Hitler' : 'http://i.imgur.com/rYNtjiD.png',
        'Broccoli' : 'http://i.imgur.com/7mZZqln.png',
        'Monster1' : 'http://i.imgur.com/76wS3ib.png',
        'Monster2' : 'http://i.imgur.com/AUnFkau.png',
        'Monster3' : 'http://i.imgur.com/x8knnvx.png',
        'Monster4' : 'http://i.imgur.com/OPeyoah.png',
        'Monster5' : 'http://i.imgur.com/4CkY65O.png',
        'Monster6' : 'http://i.imgur.com/Zo49XMo.png',
        'Monster7' : 'http://i.imgur.com/zcLq4T9.png',
        'Monster8' : 'http://i.imgur.com/ZjY1fwP.png',
        'Monster9' : 'http://i.imgur.com/J0e55C1.png',

        'Player1' : 'http://i.imgur.com/9np3V0Z.png',
        'Player2' : 'http://i.imgur.com/7dUlrnE.png',
        'Player3' : 'http://i.imgur.com/6cuZnRq.png',
        'Player4' : 'http://i.imgur.com/HhkyvKd.png',
        'Player5' : 'http://i.imgur.com/29Xwkl3.png',

        'Laser1' : 'http://i.imgur.com/kbOI4iJ.png',
        'Laser2' : 'http://i.imgur.com/tM4jjKs.png',
        'Laser3' : 'http://i.imgur.com/xnauZwI.png',
        'Laser4' : 'http://i.imgur.com/kccijdx.png',

        'title image' : 'https://i.ytimg.com/vi/FBeYD7yFWxE/maxresdefault.jpg'
    }

    images = dict()

    def load():
        for name, url in Resources.image_urls.items():
            Resources.images[name] = simplegui.load_image(url)

class Sprite:
    def __init__(self, type, pos=(0, 0), visible=False, rotation=0, scale=Settings.player_scale):
        self.type = type
        self.pos = pos
        self.image = Resources.images[self.type]
        self.size = self.image.get_width(), self.image.get_height()
        if self.size == (0, 0): # simplegui Bug, nicht vom Spiel
            print('Yo, schon wieder... :\'(')
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
    def __init__(self, targets):
        Sprite.__init__(self, random.choice(SpaceAttack.enemy_names),
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
        vec = self.targets[0].pos[0] - self.pos[0], self.targets[0].pos[1] - self.pos[1]
        min_dist = vec[0] * vec[0] + vec[1] * vec[1]
        min_dist_index = 0
        for index, target in enumerate(self.targets[1:]):
            index += 1
            vec = target.pos[0] - self.pos[0], target.pos[1] - self.pos[1]
            dist = vec[0] * vec[0] + vec[1] * vec[1]
            if dist < min_dist:
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
        Sprite.__init__(self, random.choice(SpaceAttack.player_names),
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
        self.mov_vec = 0, 0

    def turn(self, direction):
        if direction == Player.left:
            self.rotation -= self.rot_speed
        elif direction == Player.right:
            self.rotation += self.rot_speed

    def shoot(self):
        if not self.cooldown:
            laser_pair = Laser(True, laser_skin), Laser(False, laser_skin)
            n = -sin(self.rotation - pi / 2), cos(self.rotation - pi / 2)
            d = n[0] * Settings.laser_distance, n[1] * Settings.laser_distance
            laser_pair[0].shoot((self.pos[0] + d[0], self.pos[1] + d[1]), self.rotation)
            laser_pair[1].shoot((self.pos[0] - d[0], self.pos[1] - d[1]), self.rotation)
            self.lasers.append(laser_pair)
            self.cooldown = self.max_cooldown

    def get_hit(self):
        if self.invincible_counter <= 0:
            self.score = int(self.score * Settings.player_subtraction)
            self.invincible_counter = self.invincible_max

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
        for num, laserpair in enumerate(self.lasers):
            if not laserpair[0].is_valid():
                if len(laserpair) == 1:
                    del self.lasers[num]
                else:
                    self.lasers[num] = (self.lasers[num][1],)
            elif len(laserpair) > 1 and not laserpair[1].is_valid():
                self.lasers[num] = (self.lasers[num][0],)

class SpaceAttack:
    spawncount = 0
    limit = 0

    enemy_names = ['Alien', 'Batman', 'Superman', 'Android', 'Ironman',
        'Spiderman', 'Mario', 'Ninja', 'Darth Vader', 'Stormtrooper',
        'Donald Duck', 'Mickey Mouse', 'Hitler', 'Broccoli', 'Monster1',
        'Monster2', 'Monster3', 'Monster4', 'Monster5', 'Monster6', 'Monster7',
        'Monster8', 'Monster9']

    player_names = ['Player1', 'Player2', 'Player3', 'Player4', 'Player5']
    laser_names = ['Laser1', 'Laser2', 'Laser3', 'Laser4']
    background_names = ['Background1', 'Background2']

    def __init__(self, size):
        self.size = size
        self.sprites = dict()
        self.load_background()
        self.load_players()
        self.running = False
        self.enemy_counter = 0

    def load_background(self):
        self.background_name = random.choice(self.__class__.background_names)
        self.background_sprite = Sprite(self.background_name, pos=(Settings.resolution[0] // 2, Settings.resolution[1] // 2), visible=True, scale=1.0)

    def load_players(self):
        self.sprites['Player1'] = Player(0)
        self.sprites['Player1'].pos = (self.size[0] / 2, self.size[1] / 2)
        self.sprites['Player2'] = Player(1)
        self.sprites['Player2'].pos = (self.size[0] / 2, self.size[1] / 2)

    def start(self):
        self.running = True

    def update(self):
        self.spawncounter()
        if self.running:
            for name, sprite in self.sprites.items():
                sprite.update()
            for player in ('Player1', 'Player2'):
                player_sprite = self.sprites[player]
                for num, laserpair in enumerate(player_sprite.lasers):
                    if not laserpair:
                        del player_sprite.lasers[num]
                        continue
                    if len(laserpair) == 1:
                        laserpair[0].update()
                    else:
                        laserpair[0].update()
                        laserpair[1].update()
                    for lnum, laser in enumerate(laserpair):
                        for name, sprite in self.sprites.items():
                            ssize = sprite.rl_size
                            lsize = laser.rl_size
                            spos = (sprite.pos[0] - ssize[0] * 0.5, sprite.pos[1] - ssize[1] * 0.5)
                            lpos = (laser.pos[0] - lsize[0] * 0.5, laser.pos[1] - lsize[1] * 0.5)
                            if (name[:5] == 'Enemy' and
                                spos[0] < lpos[0] + lsize[0] and
                                spos[0] + ssize[0] > lpos[0] and
                                spos[1] < lpos[1] + lsize[1] and
                                spos[1] + ssize[1] > lpos[1]):
                                    del self.sprites[name]
                                    if len(laserpair) == 1:
                                        del laserpair
                                    else:
                                        player_sprite.lasers[num] = (laserpair[0 if lnum else 1],)
                                    player_sprite.score += 100
                if player_sprite.pos[0] < 0 or player_sprite.pos[0] > Settings.resolution[0] or player_sprite.pos[1] < 0 or player_sprite.pos[1] > Settings.resolution[1]:
                    if Settings.wraparound:
                        if player_sprite.pos[0] < 0:
                            player_sprite.pos = Settings.resolution[0], player_sprite.pos[1]
                        elif player_sprite.pos[0] > Settings.resolution[0]:
                            player_sprite.pos = 0, player_sprite.pos[1]
                        elif player_sprite.pos[1] < 0:
                            player_sprite.pos = player_sprite.pos[0], Settings.resolution[1]
                        elif player_sprite.pos[1] > Settings.resolution[1]:
                            player_sprite.pos = player_sprite.pos[0], 0
                    else:
                        player_sprite.get_hit()
                        player_sprite.pos = Settings.resolution[0] // 2, Settings.resolution[1] // 2
                if (player_sprite.invincible_counter // 30) % 2:
                    player_sprite.visible = False
                else:
                    player_sprite.visible = True
                psize = player_sprite.rl_size
                ppos = (player_sprite.pos[0] - psize[0] * 0.5, player_sprite.pos[1] - psize[1] * 0.5)
                for name, enemy in self.sprites.items():
                    if name[:5] == 'Enemy':
                        esize = enemy.rl_size
                        epos = (enemy.pos[0] - esize[0] * 0.5, enemy.pos[1] - esize[1] * 0.5)
                        if (ppos[0] < epos[0] + esize[0] and
                            ppos[0] + psize[0] > epos[0] and
                            ppos[1] < epos[1] + esize[1] and
                            ppos[1] + psize[1] > epos[1]):
                                player_sprite.get_hit()

    def draw(self, canvas):
        if self.running:
            self.background_sprite.draw(canvas)
            for name, sprite in self.sprites.items():
                sprite.draw(canvas)
            for laserpair in self.sprites['Player1'].lasers + self.sprites['Player2'].lasers:
                laserpair[0].draw(canvas)
                if len(laserpair) > 1:
                    laserpair[1].draw(canvas)
            canvas.draw_text(str(self.sprites['Player1'].score), (Settings.resolution[0] * 0.5 - 100, 40), 30, 'Red', 'sans-serif')
            canvas.draw_text(str(self.sprites['Player2'].score), (Settings.resolution[0] * 0.5 + 100, 40), 30, 'Blue', 'sans-serif')

    def keydown_handler(self, key):
        if key == simplegui.KEY_MAP['a']:
            self.sprites['Player1'].is_turnleft = True
        elif key == simplegui.KEY_MAP['d']:
            self.sprites['Player1'].is_turnright = True
        elif key == simplegui.KEY_MAP['left']:
            self.sprites['Player2'].is_turnleft = True
        elif key == simplegui.KEY_MAP['right']:
            self.sprites['Player2'].is_turnright = True
        elif key == simplegui.KEY_MAP['space']:
            self.sprites['Player1'].shoot()
        elif key == 13:
            self.sprites['Player2'].shoot()
        elif key == 27:
            exit(0)

    def keyup_handler(self, key):
        if key == simplegui.KEY_MAP['a']:
            self.sprites['Player1'].is_turnleft = False
        elif key == simplegui.KEY_MAP['d']:
            self.sprites['Player1'].is_turnright = False
        elif key == simplegui.KEY_MAP['left']:
            self.sprites['Player2'].is_turnleft = False
        elif key == simplegui.KEY_MAP['right']:
            self.sprites['Player2'].is_turnright = False

    def spawncounter(self):
        self.spawncount -= 1
        if self.spawncount <= 0:
            enemy = Enemy((self.sprites['Player1'], self.sprites['Player2']))
            enemy.spawn()
            self.sprites['Enemy' + str(self.enemy_counter)] = enemy
            self.enemy_counter += 1
            self.limit = Settings.growth_min_limit + (Settings.growth_max_limit - Settings.growth_min_limit) * exp(-self.enemy_counter * Settings.growth_const)
            self.spawncount = self.limit

class Button:
    modi = ('Hardmode', 'Classic 10 Lifes', 'Classic 5 Lifes', 'Classic 3 Lifes', 'Time')

    def __init__(self, pos, size, text, screen, grayed_out=False):
        self.rel_pos = pos
        self.rel_size = size
        self.pos = pos[0] * Settings.resolution[0], pos[1] * Settings.resolution[1]
        self.size = size[0] * Settings.resolution[0], size[1] * Settings.resolution[1]
        self.text = text
        self.grayed_out = grayed_out
        self.screen = screen
        self.border = True

    def draw(self, canvas):
        canvas.draw_polygon([
                self.pos,
                (self.pos[0] + self.size[0], self.pos[1]),
                (self.pos[0] + self.size[0], self.pos[1] + self.size[1]),
                (self.pos[0], self.pos[1] + self.size[1]),
            ], 4 if self.border else 1, '#ffffff', '#cccccc' if self.grayed_out else '#061c54')
        canvas.draw_text(self.text, (self.pos[0] + 10, self.pos[1] + self.size[1] * 3 / 4), self.size[1] // 2, 'White', 'sans-serif')

    def event(self):
        pass

    def point_collision(self, c):
        return ((c[0] >= self.pos[0]) and (c[0] <= self.pos[0] + self.size[0]) and
            (c[1] >= self.pos[1]) and (c[1] <= self.pos[1] + self.size[1]))

    def single_multiplayer_event(self):
        players = [str(i) + ' Player' + ('s' if i > 1 else '') for i in (2, 1)]
        self.text = players[players.index(self.text) - 1]
        if self.text == '1 Player':
            self.screen.buttons['Skin2'].grayed_out = True
            self.screen.buttons['Skin2'].pskin_button.grayed_out = True
            self.screen.buttons['Skin2'].lskin_button.grayed_out = True
        elif self.text == '2 Players':
            self.screen.buttons['Skin2'].grayed_out = False
            self.screen.buttons['Skin2'].pskin_button.grayed_out = False
            self.screen.buttons['Skin2'].lskin_button.grayed_out = False

    def modi_event(self):
        modi = [i for i in self.modi]
        # Classic: Highscore
        # Time: Highscore mit Timer
        # Hardmode: Highscore, nur 1 Leben
        self.text = modi[modi.index(self.text) - 1]
        if self.text in ('Classic 10 Lifes', 'Classic 5 Lifes', 'Classic 3 Lifes', 'Hardmode'):
            self.screen.buttons['Time'].grayed_out = True
        elif self.text in ('Time',):
            self.screen.buttons['Time'].grayed_out = False

    def start(self):
        window.start_game()

    def time_event(self):
        times = ['Time: ' + str(i) + 'min' for i in (10, 5, 2, 1)]
        self.text = times[times.index(self.text) - 1]

class ImageButton(Button):
    def __init__(self, images, *kwargs):
        Button.__init__(self, *kwargs)
        self.images = images
        self.image_index = 0
        self.image_sizes = tuple((i.get_width(), i.get_height()) for i in self.images)
        self.real_image_sizes = tuple((self.size[0], self.size[0] * sz[0] / sz[1]) if sz[0] > sz[1] else () for sz in self.image_sizes)
        self.event = self.switch

    def switch(self):
        self.image_index = (self.image_index + 1) % len(self.images)

    def draw(self, canvas):
        Button.draw(self, canvas)
        image_size = self.image_sizes[self.image_index]
        real_image_size = self.real_image_sizes[self.image_index]
        print(self.image_index, image_size, real_image_size)
        canvas.draw_image(self.images[self.image_index], (image_size[0] // 2, image_size[1] // 2), image_size, (self.pos[0] + real_image_size[0] / 2, self.pos[1] + real_image_size[1] / 2), real_image_size)

class SkinButton(Button):
    def __init__(self, *kwargs):
        Button.__init__(self, *kwargs)
        # Playerskin
        self.pskin_button = ImageButton(
            tuple(Resources.images[i] for i in SpaceAttack.player_names),
            (self.rel_pos[0] + self.rel_size[0] * .4, self.rel_pos[1]),
            (self.rel_size[0] * .2, self.rel_size[1]),
            '', self.screen, self.grayed_out)
        self.pskin_button.border = False
        self.pskin_button.pos = self.pskin_button.pos[0], self.pskin_button.pos[1] + 1
        self.pskin_button.size = self.pskin_button.size[0], self.pskin_button.size[1] - 2
        # Laserskin
        self.lskin_button = ImageButton(
            tuple(Resources.images[i] for i in SpaceAttack.laser_names),
            (self.rel_pos[0] + self.rel_size[0] * .7, self.rel_pos[1]),
            (self.rel_size[0] * .2, self.rel_size[1]),
            '', self.screen, self.grayed_out)
        self.lskin_button.pos = self.lskin_button.pos[0], self.lskin_button.pos[1] + 1
        self.lskin_button.size = self.lskin_button.size[0], self.lskin_button.size[1] - 2
        self.lskin_button.border = False

    def draw(self, canvas):
        Button.draw(self, canvas)
        self.pskin_button.draw(canvas)
        self.lskin_button.draw(canvas)

class TitleScreen:
    def __init__(self):
        self.title_img = Resources.images['title image']
        self.title_sz = self.title_img.get_width(), self.title_img.get_height()
        self.bg_img = Resources.images[random.choice(SpaceAttack.background_names)]
        self.bg_sz = self.bg_img.get_width(), self.bg_img.get_height()
        if self.bg_sz == (0, 0):
            print('Yo, eins scheiser dreggs Fehla... :/')
        self.buttons = {
            'Player_count' : Button((.1, .4), (.35, .1), '1 Player', self),
            'Modi' : Button((.1, .55), (.35, .1), Button.modi[-1], self),
            'Begin' : Button((.1, .7), (.35, .1), 'Begin', self),
            'Exit' : Button((.1, .85), (.35, .1), 'Exit', self),
            'Skin1' : SkinButton((.55, .4), (.35, .1), 'Player 1', self),
            'Skin2' : SkinButton((.55, .55), (.35, .1), 'Player 2', self),
            'Time' : Button((.55, .7), (.35, .1), 'Time: 1min', self)
        }
        self.buttons['Skin2'].grayed_out = True
        self.buttons['Skin2'].pskin_button.grayed_out = True
        self.buttons['Skin2'].lskin_button.grayed_out = True
        self.buttons['Player_count'].event = self.buttons['Player_count'].single_multiplayer_event
        self.buttons['Modi'].event = self.buttons['Modi'].modi_event
        self.buttons['Begin'].event = self.buttons['Begin'].start
        self.buttons['Exit'].event = exit
        self.buttons['Time'].event = self.buttons['Time'].time_event

    def keydown_handler(self, key):
        if key == 27:
            exit(0)

    def mouseclick_handler(self, pos):
        for button in self.buttons.values():
            if (not button.grayed_out) and button.point_collision(pos):
                button.event()

    def draw(self, canvas):
        canvas.draw_image(self.bg_img, (self.bg_sz[0] / 2, self.bg_sz[1] / 2), self.bg_sz, (Settings.resolution[0] / 2, Settings.resolution[1] / 2), Settings.resolution)
        canvas.draw_image(self.title_img, (self.title_sz[0] / 2, self.title_sz[1] / 2), self.title_sz, (Settings.resolution[0] / 2, .2 * self.title_sz[1] / 2), (self.title_sz[0] * .3, self.title_sz[1] * .3))
        for button in self.buttons.values():
            button.draw(canvas)

class Window:
    def __init__(self, title='NONE'):
        self.frame = simplegui.create_frame(title, Settings.resolution[0], Settings.resolution[1])
        self.frame.start()

    def start_title_screen(self):
        self.title_screen = TitleScreen()
        self.frame.set_draw_handler(self.title_screen.draw)
        self.frame.set_keydown_handler(self.title_screen.keydown_handler)
        self.frame.set_mouseclick_handler(self.title_screen.mouseclick_handler)

    def start_game(self):
        self.game = SpaceAttack(Settings.resolution)
        self.timer = simplegui.create_timer(5, self.update)
        self.frame.set_draw_handler(self.game.draw)
        self.frame.set_keydown_handler(self.game.keydown_handler)
        self.frame.set_keyup_handler(self.game.keyup_handler)
        self.timer.start()
        self.game.start()

    def update(self):
        self.game.update()

if __name__ == '__main__':
    Resources.load()
    window = Window('Space Attack')
    window.start_title_screen()
