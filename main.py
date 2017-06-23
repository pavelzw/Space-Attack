# main.py
from math import exp
import simplegui
import time
import user43_QlOAN8LSaf_7 as sprites # sprites.py
from user43_7yqHvQrReO_1 import Settings, Resources # properties.py

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
        self.music_handler()

    def load_background(self):
        self.background_name = Settings.background
        self.background_sprite = sprites.Sprite(self.background_name, pos=(Settings.resolution[0] // 2, Settings.resolution[1] // 2), visible=True, scale=1.0)

    def load_players(self):
        self.sprites['Player1'] = sprites.Player(0)
        if Settings.is_2_players:
            self.sprites['Player1'].pos = self.size[0] * 1 / 3, self.size[1] / 2
            self.sprites['Player2'] = sprites.Player(1)
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
            self.sprites['Player1'].is_turnright = False
        elif key == Settings.controls['p1_right']:
            self.sprites['Player1'].is_turnright = True
            self.sprites['Player1'].is_turnleft = False
        elif key == Settings.controls['p2_left'] and Settings.is_2_players:
            self.sprites['Player2'].is_turnleft = True
            self.sprites['Player2'].is_turnright = False
        elif key == Settings.controls['p2_right'] and Settings.is_2_players:
            self.sprites['Player2'].is_turnright = True
            self.sprites['Player2'].is_turnleft = False
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

    def music_handler(self):
        song = Settings.song
        command = Settings.music
        if command:
            Resources.sounds[song].set_volume(.5)
            Resources.sounds[song].play()
        if not command:
            Resources.sounds[song].pause()

    def spawncounter(self):
        self.spawncount -= 1
        if self.spawncount <= 0:
            if Settings.is_2_players:
                enemy = sprites.Enemy((self.sprites['Player1'], self.sprites['Player2']), SpaceAttack.enemy_names)
            else:
                enemy = sprites.Enemy((self.sprites['Player1'],), SpaceAttack.enemy_names)
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

    def adv_gen_song_pick_event(self):
        songs = [i for i in Settings.music_list]
        Settings.song = songs[songs.index(Settings.song) - 1]
        self.text = 'Song: ' + Settings.song

    def adv_gen_music_event(self):
        if Settings.music:
            Settings.music = False
            self.screen.buttons['current_song'].grayed_out = True
        else:
            Settings.music = True
            self.screen.buttons['current_song'].grayed_out = False
        self.text = 'Music: ' + ('On' if Settings.music else 'Off')

    def adv_gen_sounds_event(self):
        if Settings.sounds:
            Settings.sounds = False
        else:
            Settings.sounds = True
        self.text = 'Sounds: ' + ('On' if Settings.sounds else 'Off')

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
        self.title_img = Resources.images['Logo']
        self.title_sz = self.title_img.get_width(), self.title_img.get_height()
        if self.title_sz[0] == 0 or self.title_sz[1] == 0:
            print('SimpleGUI Fehler')
        self.title_real_sz = (Settings.resolution[1] * .25 / self.title_sz[1]
        * self.title_sz[0], Settings.resolution[1] * .25)
        self.title_pos = (Settings.resolution[0] / 2, Settings.resolution[1] * .2)
        self.bg_img = Resources.images[Settings.background]
        self.bg_sz = self.bg_img.get_width(), self.bg_img.get_height()
        if self.bg_sz == (0, 0):
            print('SimpleGUI-Fehler')
        self.init_buttons()

    def init_buttons(self):
        Resources.load_buttons(self.name, Button, ImageButton, SpaceAttack.player_names, SpaceAttack.laser_names)
        self.button_set = ButtonSet(self.name)

    def keydown_handler(self, key):
        if key == Settings.controls['end']:
            exit(0)

    def mouseclick_handler(self, pos):
        self.button_set.onclick(pos)

    def draw(self, canvas):
        canvas.draw_image(self.bg_img, (self.bg_sz[0] / 2, self.bg_sz[1] / 2), self.bg_sz, (Settings.resolution[0] / 2, Settings.resolution[1] / 2), Settings.resolution)
        canvas.draw_image(self.title_img,
            (self.title_sz[0] / 2, self.title_sz[1] / 2),
            self.title_sz,
            self.title_pos,
            self.title_real_sz)
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
    Resources.load_sounds()
    window = Window(Settings.title)
    window.start_menu()
