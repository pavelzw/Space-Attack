from math import pi, sin, cos, sqrt, exp
import random
import simplegui
import time

class Settings:
    title = 'Space Attack'
    resolution = 1280, 720
    blue = '#0d36e3' # Rot, das im gesamten Spiel verwendet wird
    red = '#d01306' # Blau, das im gesamten Spiel verwendet wird
    player_velocity = 1.5 # Geschwindigkeit des Spielers
    player_angular_velocity = pi / 180 # Geschwindigkeit, mit der sich Spieler dreht
    player_scale = .1 # Spieler ist 1/10 von Höhe groß
    player_cooldown = 50
    player_invulnerability_time = 450 # Zeit, die der Spieler unbesiegbar ist, nachdem er getroffen wurde
    player_subtraction = 0.75 # Faktor, der abgezogen wird, wenn Spieler getroffen
    enemy_scale = .1 # Gegner ist 1/10 von Höhe groß
    enemy_velocity = .5 # Geschwindigkeit der Gegner
    laser_scale = .03 # Laser ist 0.03 von Höhe groß
    laser_velocity = 6 # Geschwindigkeit der Laser
    laser_distance = resolution[1] * player_scale * .4 # Abstand zwischen Lasern
    growth_max_limit = 1000 # maximale Gegnerspawntime (ms)
    growth_min_limit = 200 # minimale Gegnerspawntime (ms)
    growth_const = 0.06 # Konstante, mit der Gegnerspawntime exponentiell zunimmt
    player1_laser = 'Laser1'
    player2_laser = 'Laser1'
    player1_skin = 'Player1'
    player2_skin = 'Player1'
    background = 'Background1'
    controls = {
        'p1_left' : simplegui.KEY_MAP['a'],
        'p1_right' : simplegui.KEY_MAP['d'],
        'p1_shoot' : simplegui.KEY_MAP['space'],
        'p2_left' : simplegui.KEY_MAP['left'],
        'p2_right' : simplegui.KEY_MAP['right'],
        'p2_shoot' : 13,
        'end' : 27,
        }
    # GAMEMODES
    modi = ('Hardmode', 'Classic 10 Lifes', 'Classic 5 Lifes', 'Classic 3 Lifes', 'Time')
    modus = modi[-1]
    has_lifes = False
    is_time_mode = True
    max_time = 60
    is_2_players = True

    # ADVANCED SETTINGS
    wraparound = True  # rechts raus, links wieder rein
    resolution_list = {
        #'4K' : (3840, 2160),
        'Full HD' : (1920, 1080),
        'HD' : (1280, 720)
        }

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
        'Laser4' : 'http://i.imgur.com/2oXXUh0.png',

        'title image' : 'http://i.imgur.com/TgbmCNg.png'
    }

    images = dict()

    button_sets = dict()

    def load():
        for name, url in Resources.image_urls.items():
            Resources.images[name] = simplegui.load_image(url)

    def load_buttons(name):
        player_images = dict()
        laser_images = dict()
        for i in SpaceAttack.player_names:
            player_images[i] = Resources.images[i]
        for i in SpaceAttack.laser_names:
            laser_images[i] = Resources.images[i]
        if name == 'main_menu':
            Resources.button_sets[name] = {
                'Player_count' : [Button, (.1, .4), (.35, .1), '2 Players' if Settings.is_2_players else '1 Player', Button.single_multiplayer_event, False],
                'Modi' : [Button, (.1, .55), (.35, .1), Settings.modus, Button.modi_event, False],
                'Begin' : [Button, (.1, .7), (.35, .1), 'Begin', Button.start_event, False],
                'Exit' : [Button, (.1, .85), (.35, .1), 'Exit', exit, False],
                'Skin1' : [Button, (.55, .4), (.35, .1), 'Player 1', Button.pass_event, False],
                'Skin2' : [Button, (.55, .55), (.35, .1), 'Player 2', Button.pass_event, False],
                'Skin1Player' : [ImageButton, True, True, (.70, .4), (.1, .1), ImageButton.switch, player_images, False],
                'Skin1Laser' : [ImageButton, True, False, (.80, .4), (.1, .1), ImageButton.switch, laser_images, False],
                'Skin2Player' : [ImageButton, False, True, (.70, .55), (.1, .1), ImageButton.switch, player_images, False],
                'Skin2Laser' : [ImageButton, False, False, (.80, .55), (.1, .1), ImageButton.switch, laser_images, False],
                'Time' : [Button, (.55, .7), (.35, .1), 'Time: %imin' % (Settings.max_time // 60), Button.time_event, False],
                'adv. settings' : [Button, (.55, .85), (.35, .1), 'Advanced Settings', Button.adv_settings_event, False]
            }
            if Resources.button_sets[name]['Player_count'][3] == '1 Player':
                Resources.button_sets[name]['Skin2'][-1] = True
                Resources.button_sets[name]['Skin2Player'][-1] = True
                Resources.button_sets[name]['Skin2Laser'][-1] = True
            if Resources.button_sets[name]['Modi'][3] != 'Time':
                Resources.button_sets[name]['Time'][-1] = True
        elif name == 'adv_settings':
            Resources.button_sets[name] = {
                'general' :
                    [Button, (.1, .4), (.8, .1), 'General Settings',
                    Button.adv_general_event, False],
                'items' :
                    [Button, (.1, .55), (.8, .1), 'Item Settings',
                    Button.adv_items_event, False],
                'controls' :
                    [Button, (.1, .7), (.8, .1), 'Controls',
                    Button.adv_controls_event, False],
                'back' :
                    [Button, (.1, .85), (.8, .1), 'Back',
                    Button.adv_back_event, False],
            }
        elif name == 'adv_general':
            Resources.button_sets[name] = {
                'resolution' :
                    [Button, (.1, .4), (.8, .1),
                    'Resolution: %s'
                    % Settings.resolution_list.keys()[Settings.resolution_list.values().index(Settings.resolution)], # hier soll der zugehörige String zur Auflösung gefunden werden... bei dicts klappt kein .index()
                    Button.adv_gen_res_event, False],
                'background' :
                    [Button, (.1, .55), (.8, .1), 'Change background',
                    Button.adv_gen_change_background_event, False],
                'wraparound' :
                    [Button, (.1, .70), (.8, .1),
                    'Wraparound: ' + ('On' if Settings.wraparound else 'Off'),
                    Button.adv_gen_wraparound_event, False],
                'back' :
                    [Button, (.1, .85), (.8, .1), 'Back',
                    Button.adv_back_event, False]
            }
        elif name == 'adv_items': # todo
            Resources.button_sets[name] = {
                'back' :
                    [Button, (.1, .85), (.8, .1), 'Back',
                    Button.adv_back_event, False]
            } # todo
        elif name == 'adv_controls': # todo
            Resources.button_sets[name] = {
                'p1_left' : [Button, (.1, .4), (.35, .1), 'Player 1 Left: ', Button.pass_event, False],
                'p1_right' : [Button, (.1, .55), (.35, .1), 'Player 1 Right: ', Button.pass_event, False],
                'p1_shoot' : [Button, (.1, .7), (.35, .1), 'Player 1 Shoot: ', Button.pass_event, False],
                'p2_left' : [Button, (.55, .4), (.35, .1), 'Player 2 Left: ', Button.pass_event, False],
                'p2_right' : [Button, (.55, .55), (.35, .1), 'Player 2 Right: ', Button.pass_event, False],
                'p2_shoot' : [Button, (.55, .7), (.35, .1), 'Player 2 Shoot: ', Button.pass_event, False],
                'back' :
                    [Button, (.1, .85), (.8, .1), 'Back',
                    Button.adv_back_event, False]
                #simplegui.KEY_MAP.keys()[simplegui.KEY_MAP.values().index(key)]
                #'p1_left' : [Button, (.1, .4), (.35, .1), 'Player 1 Left: %s' %s simplegui.KEY_MAP.values(65)]
            }

        else:
            raise KeyError('the menu key "%s" is not present' % name)

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
        self.any_alive = True

    def load_background(self):
        self.background_name = Settings.background
        self.background_sprite = Sprite(self.background_name, pos=(Settings.resolution[0] // 2, Settings.resolution[1] // 2), visible=True, scale=1.0)

    def load_players(self):
        self.sprites['Player1'] = Player(0)
        if Settings.is_2_players:
            self.sprites['Player1'].pos = self.size[0] * 1 / 3, self.size[1] / 2
            self.sprites['Player2'] = Player(1)
            self.sprites['Player2'].pos = self.size[0] * 2 / 3, self.size[1] / 2
        else:
            self.sprites['Player1'].pos = self.size[0] * 1 / 2, self.size[1] / 2

    def start(self):
        self.running = True
        self.timer = time.time()

    def update(self):
        self.spawncounter()
        if self.running:
            for name, sprite in self.sprites.items():
                sprite.update()
            alive_players = []
            for i in ('Player1', 'Player2') if Settings.is_2_players else ('Player1',):
                if self.sprites[i].alive:
                    alive_players.append(i)
            any_alive = False
            for player in alive_players:
                any_alive = True
                player_sprite = self.sprites[player]
                for num, laser in enumerate(player_sprite.lasers):
                    laser.update()
                    for name, sprite in self.sprites.items():
                        if name[:5] != 'Enemy': continue
                        ssize = sprite.rl_size
                        lsize = laser.rl_size
                        spos = sprite.pos[0] - ssize[0] * 0.5, sprite.pos[1] - ssize[1] * 0.5
                        lpos = laser.pos[0] - lsize[0] * 0.5, laser.pos[1] - lsize[1] * 0.5
                        if (spos[0] < lpos[0] + lsize[0] and
                            spos[0] + ssize[0] > lpos[0] and
                            spos[1] < lpos[1] + lsize[1] and
                            spos[1] + ssize[1] > lpos[1]):
                                del self.sprites[name]
                                del laser
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
                if Settings.is_time_mode and time.time() >= Settings.max_time + self.timer:
                    self.sprites['Player1'].die()
                    if Settings.is_2_players:
                        self.sprites['Player2'].die()
            self.any_alive = any_alive

    def draw(self, canvas):
        two_players = Settings.is_2_players
        if self.running:
            self.background_sprite.draw(canvas)
            for name, sprite in self.sprites.items():
                if self.any_alive:
                    sprite.draw(canvas)
            p1score = self.sprites['Player1'].score
            if two_players:
                p2score = self.sprites['Player2'].score
            if not self.any_alive:
                if two_players:
                    canvas.draw_text(str(p1score), (Settings.resolution[0] * 0.5 - 300, 130), 120, Settings.red, 'sans-serif')
                    canvas.draw_text(str(p2score), (Settings.resolution[0] * 0.5 + 300, 130), 120, Settings.blue, 'sans-serif')
                    if p1score > p2score:
                        canvas.draw_text('Player 1 won the game!', (Settings.resolution[0] * 0.5 - 380, Settings.resolution[1] // 2), 70, '#aaaabb', 'sans-serif')
                    elif p1score < p2score:
                        canvas.draw_text('Player 2 won the game!', (Settings.resolution[0] * 0.5 - 380, Settings.resolution[1] // 2), 70, '#aaaabb', 'sans-serif')
                    elif p1score == p2score:
                        canvas.draw_text('draw', (Settings.resolution[0] * 0.5 - 50, Settings.resolution[1] // 2), 70, '#aaaabb', 'sans-serif')
                else:
                    canvas.draw_text(str(p1score), (Settings.resolution[0] * 0.5 - 100, 130), 140, 'White', 'sans-serif')
                    canvas.draw_text('Game Over', (Settings.resolution[0] * 0.5 - 200, Settings.resolution[1] // 2), 70, '#aaaabb', 'sans-serif')
            else:
                if two_players:
                    canvas.draw_text(str(p1score), (Settings.resolution[0] * 0.5 - 100, 40), 30, Settings.red, 'sans-serif')
                    canvas.draw_text(str(p2score), (Settings.resolution[0] * 0.5 + 100, 40), 30, Settings.blue, 'sans-serif')
                else:
                    canvas.draw_text(str(p1score), (Settings.resolution[0] * 0.5 - 40, 40), 40, Settings.red, 'sans-serif')
            if Settings.is_time_mode and (self.sprites['Player1'].alive or (two_players and self.sprites['Player2'].alive)):
                canvas.draw_text(str(int(round(Settings.max_time - time.time() + self.timer))), (10, 45), 40, '#eeeeff', 'sans-serif')

    def keydown_handler(self, key):
        if key == Settings.controls['p1_left']:
            self.sprites['Player1'].is_turnleft = True
        elif key == Settings.controls['p1_right']:
            self.sprites['Player1'].is_turnright = True
        elif key == Settings.controls['p2_left'] and Settings.is_2_players:
            self.sprites['Player2'].is_turnleft = True
        elif key == Settings.controls['p2_right'] and Settings.is_2_players:
            self.sprites['Player2'].is_turnright = True
        elif key == Settings.controls['p1_shoot']:
            self.sprites['Player1'].shoot()
        elif key == Settings.controls['p2_shoot'] and Settings.is_2_players:
            self.sprites['Player2'].shoot()
        elif key == Settings.controls['end']:
            exit(0)

    def keyup_handler(self, key):
        if key == Settings.controls['p1_left']:
            self.sprites['Player1'].is_turnleft = False
        elif key == Settings.controls['p1_right']:
            self.sprites['Player1'].is_turnright = False
        elif key == Settings.controls['p2_left'] and Settings.is_2_players:
            self.sprites['Player2'].is_turnleft = False
        elif key == Settings.controls['p2_right'] and Settings.is_2_players:
            self.sprites['Player2'].is_turnright = False

    def spawncounter(self):
        self.spawncount -= 1
        if self.spawncount <= 0:
            if Settings.is_2_players:
                enemy = Enemy((self.sprites['Player1'], self.sprites['Player2']))
            else:
                enemy = Enemy((self.sprites['Player1'],))
            enemy.spawn()
            self.sprites['Enemy' + str(self.enemy_counter)] = enemy
            self.enemy_counter += 1
            self.limit = Settings.growth_min_limit + (Settings.growth_max_limit - Settings.growth_min_limit) * exp(-self.enemy_counter * Settings.growth_const)
            self.spawncount = self.limit

class Button:
    def __init__(self, pos, size, text, screen, grayed_out=False, event=None):
        self.rel_pos = pos
        self.rel_size = size
        self.pos = pos[0] * Settings.resolution[0], pos[1] * Settings.resolution[1]
        self.size = size[0] * Settings.resolution[0], size[1] * Settings.resolution[1]
        self.text = text
        self.grayed_out = grayed_out
        self.screen = screen
        self.border = True
        self.event = event

    def draw(self, canvas):
        canvas.draw_polygon([
                self.pos,
                (self.pos[0] + self.size[0], self.pos[1]),
                (self.pos[0] + self.size[0], self.pos[1] + self.size[1]),
                (self.pos[0], self.pos[1] + self.size[1]),
            ], 4 if self.border else 1, '#ffffff', '#cccccc' if self.grayed_out else '#061c54')
        canvas.draw_text(self.text, (self.pos[0] + 10, self.pos[1] + self.size[1] * 3 / 4), self.size[1] // 2, 'White', 'sans-serif')

    def point_collision(self, c):
        return ((c[0] >= self.pos[0]) and (c[0] <= self.pos[0] + self.size[0]) and
            (c[1] >= self.pos[1]) and (c[1] <= self.pos[1] + self.size[1]))

    def event(self):
        pass

    def pass_event(self):
        pass

    def single_multiplayer_event(self):
        players = [str(i) + ' Player' + ('s' if i > 1 else '') for i in (1, 2)]
        self.text = players[players.index(self.text) - 1]
        if self.text == '1 Player':
            self.screen.buttons['Skin2'].grayed_out = True
            self.screen.buttons['Skin2Player'].grayed_out = True
            self.screen.buttons['Skin2Laser'].grayed_out = True
            Settings.is_2_players = False
        elif self.text == '2 Players':
            self.screen.buttons['Skin2'].grayed_out = False
            self.screen.buttons['Skin2Player'].grayed_out = False
            self.screen.buttons['Skin2Laser'].grayed_out = False
            Settings.is_2_players = True

    def modi_event(self):
        modi = [i for i in Settings.modi]
        # Classic: Highscore
        # Time: Highscore mit Timer
        # Hardmode: Highscore, nur 1 Leben
        self.text = modi[modi.index(self.text) - 1]
        if self.text in ('Classic 10 Lifes', 'Classic 5 Lifes', 'Classic 3 Lifes', 'Hardmode'):
            self.screen.buttons['Time'].grayed_out = True
            Settings.has_lifes = True
            Settings.is_time_mode = False
        elif self.text in ('Time',):
            self.screen.buttons['Time'].grayed_out = False
            Settings.has_lifes = False
            Settings.is_time_mode = True
        Settings.modus = self.text

    def start_event(self):
        window.start_game()

    def time_event(self):
        times = ['Time: ' + str(i) + 'min' for i in (10, 5, 2, 1)]
        self.text = times[times.index(self.text) - 1]
        Settings.max_time = int(self.text[6:-3]) * 60

    def adv_back_event(self):
        window.start_menu('main_menu')

    def adv_settings_event(self):
        window.start_menu('adv_settings')

    def adv_general_event(self):
        window.start_menu('adv_general')

    def adv_items_event(self):
        window.start_menu('adv_items')

    def adv_controls_event(self):
        window.start_menu('adv_controls')

    def adv_gen_res_event(self):
        if False: #hier wuerde nur ein schwarzer Screen kommen
            res_list = Settings.resolution_list
            keys=res_list.keys()
            values=res_list.values()
            new_res_text = keys[values.index(Settings.resolution) - 1]
            Settings.resolution = res_list[new_res_text]
            self.text = 'Resolution: ' + new_res_text
            window.frame = simplegui.create_frame(Settings.title, Settings.resolution[0], Settings.resolution[1])
            window.frame.start()

    def adv_gen_change_background_event(self):
        backgrounds = SpaceAttack.background_names
        Settings.background = backgrounds[backgrounds.index(Settings.background) - 1]
        window.game.bg_img = Resources.images[Settings.background]

    def adv_gen_wraparound_event(self):
        if Settings.wraparound:
            Settings.wraparound = False
        else:
            Settings.wraparound = True
        self.text = 'Wraparound: ' + ('On' if Settings.wraparound else 'Off')

class ImageButton(Button):
    def __init__(self, images, is_player1, is_player_skin, *kwargs):
        Button.__init__(self, *kwargs)
        self.images = images
        self.indices = list(images.keys())
        self.image_index = 0
        self.image_sizes = tuple((i.get_width(), i.get_height()) for i in self.images.values())
        aspect_ratio = self.size[0] / self.size[1]
        self.real_image_sizes = tuple((self.size[0], self.size[0] * sz[1] / sz[0]) if sz[0] / sz[1] > aspect_ratio else (self.size[1] * sz[0] / sz[1], self.size[1]) for sz in self.image_sizes)
        self.event = self.switch
        self.is_player1, self.is_player_skin = is_player1, is_player_skin

    def switch(self):
        self.image_index = (self.image_index + 1) % len(self.images)
        if self.is_player1:
            if self.is_player_skin:
                Settings.player1_skin = self.indices[self.image_index]
            else:
                Settings.player1_laser = self.indices[self.image_index]
        else:
            if self.is_player_skin:
                Settings.player2_skin = self.indices[self.image_index]
            else:
                Settings.player2_laser = self.indices[self.image_index]

    def draw(self, canvas):
        Button.draw(self, canvas)
        image_size = self.image_sizes[self.image_index]
        real_image_size = self.real_image_sizes[self.image_index]
        canvas.draw_image(self.images[self.indices[self.image_index]],
            (image_size[0] // 2, image_size[1] // 2),
            image_size,
            (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2),
            (real_image_size[0] - 5, real_image_size[1] - 5))

class ButtonSet:
    def __init__(self, name):
        self.name = name
        self.buttons = dict()
        for bname, args in Resources.button_sets[name].items():
            if args[0] == Button:
                self.buttons[bname] = args[0](args[1], args[2], args[3], self, grayed_out=args[-1], event=args[4])
            elif args[0] == ImageButton:
                self.buttons[bname] = args[0](args[6], args[1], args[2], args[3], args[4], '', self, args[-1], args[5])

    def onclick(self, pos):
        for button in self.buttons.values():
            if (not button.grayed_out) and button.point_collision(pos):
                # komischer Fehler
                if button.__class__ == Button:
                    button.event(button) # Button will noch self mit bekommen
                elif button.__class__ == ImageButton:
                    button.event() # ImageButton will self nicht haben

    def draw(self, canvas):
        for button in self.buttons.values():
            button.draw(canvas)

class Menu:
    def __init__(self, name):
        self.name = name
        self.title_img = Resources.images['title image']
        self.title_sz = self.title_img.get_width(), self.title_img.get_height()
        self.bg_img = Resources.images[Settings.background]
        self.bg_sz = self.bg_img.get_width(), self.bg_img.get_height()
        if self.bg_sz == (0, 0):
            print('SimpleGUI-Fehler')
        self.init_buttons()

    def init_buttons(self):
        Resources.load_buttons(self.name)
        self.button_set = ButtonSet(self.name)

    def keydown_handler(self, key):
        if key == Settings.controls['end']:
            exit(0)

    def mouseclick_handler(self, pos):
        self.button_set.onclick(pos)

    def draw(self, canvas):
        canvas.draw_image(self.bg_img, (self.bg_sz[0] / 2, self.bg_sz[1] / 2), self.bg_sz, (Settings.resolution[0] / 2, Settings.resolution[1] / 2), Settings.resolution)
        canvas.draw_image(self.title_img, (self.title_sz[0] / 2, self.title_sz[1] / 2), self.title_sz, (Settings.resolution[0] / 2, .2 * self.title_sz[1] / 2), (self.title_sz[0] * .3, self.title_sz[1] * .3))
        self.button_set.draw(canvas)

class Window:
    def __init__(self, title='NONE'):
        self.frame = simplegui.create_frame(title, Settings.resolution[0], Settings.resolution[1])
        self.frame.start()

    def start_menu(self, name='main_menu'):
        self.game = Menu(name)
        self.frame.set_draw_handler(self.game.draw)
        self.frame.set_keydown_handler(self.game.keydown_handler)
        self.frame.set_mouseclick_handler(self.game.mouseclick_handler)

    def start_game(self):
        self.game = SpaceAttack(Settings.resolution)
        self.timer = simplegui.create_timer(5, self.update)
        self.frame.set_draw_handler(self.game.draw)
        self.frame.set_keydown_handler(self.game.keydown_handler)
        self.frame.set_keyup_handler(self.game.keyup_handler)
        # lambda: leere Funktion, die nix macht
        self.frame.set_mouseclick_handler(lambda pos:None)
        self.timer.start()
        self.game.start()

    def update(self):
        self.game.update()

if __name__ == '__main__':
    Resources.load()
    window = Window(Settings.title)
    window.start_menu()
