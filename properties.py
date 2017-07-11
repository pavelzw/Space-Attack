# properties.py
from math import pi
import simplegui
import random

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
        'end' : 27
        }
    # GAMEMODES
    modi = ('Hardmode', 'Classic 10 Lifes', 'Classic 5 Lifes', 'Classic 3 Lifes', 'Time')
    modus = modi[-1]
    has_lifes = False
    is_time_mode = True
    max_time = 60
    is_2_players = True

    # ADVANCED SETTINGS
    music_list = ('Gravity Falls', 'Battle Against True Hero', 'Bonetrousle',
        'Megalovania', 'Asgore Theme', 'Moon Theme')
    song = random.choice(music_list)
    music = True
    sounds = True
    wraparound = True  # rechts raus, links wieder rein
    resolution_list = {
        '4K' : (3840, 2160),
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

        'Logo' : 'http://i.imgur.com/3CbkPD6.png'
    }

    sound_urls = {
        'Laser' : 'http://k003.kiwi6.com/hotlink/htcy8y6r9z/laser1_Gun.flac',

        'Gravity Falls' : 'http://k003.kiwi6.com/hotlink/8uhh54qrlv/Gravity_Falls_Theme_Extended_8-bit_mix_.mp3',
        'Battle Against True Hero' : 'http://k003.kiwi6.com/hotlink/v4vaesgl3y/Undertale_-_Battle_Against_a_True_Hero.mp3',
        'Bonetrousle' : 'http://k003.kiwi6.com/hotlink/xlvl2x4otr/Undertale_-_Bonetrousle.mp3',
        'Megalovania' : 'http://k003.kiwi6.com/hotlink/xsocelu5qq/Undertale_-_Megalovania.mp3',
        'Asgore Theme' : 'http://k003.kiwi6.com/hotlink/81ddl0tzw1/Undertale_Asgore_Theme.mp3',
        'Moon Theme' : 'http://k003.kiwi6.com/hotlink/lds54k47u2/Ducktales_Remastered_Soundtrack_-_Moon_Theme.mp3'
    }

    images = dict()

    button_sets = dict()

    sounds = dict()

    def load():
        for name, url in Resources.image_urls.items():
            Resources.images[name] = simplegui.load_image(url)

    def load_buttons(name, Button, ImageButton, player_names, laser_names):
        player_images = dict()
        laser_images = dict()
        for i in player_names:
            player_images[i] = Resources.images[i]
        for i in laser_names:
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
                'adv. settings' : [Button, (.55, .85), (.35, .1), 'Advanced Settings', Button.adv_general_event, False] # eig adv_back_event, aber nicht genug Einstellungen
            }
            if Resources.button_sets[name]['Player_count'][3] == '1 Player':
                Resources.button_sets[name]['Skin2'][-1] = True
                Resources.button_sets[name]['Skin2Player'][-1] = True
                Resources.button_sets[name]['Skin2Laser'][-1] = True
            if Resources.button_sets[name]['Modi'][3] != 'Time':
                Resources.button_sets[name]['Time'][-1] = True
#        elif name == 'adv_settings':
#            Resources.button_sets[name] = {
#                'general' :
#                    [Button, (.1, .4), (.8, .1), 'General Settings',
#                    Button.adv_general_event, False],
#                'items' :
#                    [Button, (.1, .55), (.8, .1), 'Item Settings',
#                    Button.adv_items_event, False],
#                'controls' :
#                    [Button, (.1, .7), (.8, .1), 'Controls',
#                    Button.adv_controls_event, False],
#                'back' :
#                    [Button, (.1, .85), (.8, .1), 'Back',
#                    Button.adv_back_event, False],
#            }
        elif name == 'adv_general':
            Resources.button_sets[name] = {
#                'resolution' :
#                    [Button, (.1, .4), (.35, .1),
#                    'Resolution: %s'
#                    % Settings.resolution_list.keys()[Settings.resolution_list.values().index(Settings.resolution)], # hier soll der zugehörige String zur Auflösung gefunden werden... bei dicts klappt kein .index()
#                    Button.adv_gen_res_event, False],
                'background' :
                    [Button, (.1, .55), (.35, .1), 'Change background',
                    Button.adv_gen_change_background_event, False],
                'wraparound' :
                    [Button, (.1, .7), (.35, .1),
                    'Wraparound: ' + ('On' if Settings.wraparound else 'Off'),
                    Button.adv_gen_wraparound_event, False],
                'current_song' :
                    [Button, (.1, .4), (.8, .1), # eig nur die Hälfte groß, auf andere Seite kommt Resolution
                    'Song: ' + Settings.song,
                    Button.adv_gen_song_pick_event, False],
                'music' :
                    [Button, (.55, .55), (.35, .1),
                    'Music: ' + ('On' if Settings.music else 'Off'),
                    Button.adv_gen_music_event, False],
                'sounds' :
                    [Button, (.55, .7), (.35, .1),
                    'Sounds: ' + ('On' if Settings.sounds else 'Off'),
                    Button.adv_gen_sounds_event, False],
                'back' :
                    [Button, (.1, .85), (.8, .1), 'Back',
                    Button.adv_back_event, False]
            }
            if Resources.button_sets[name]['music'][3] == 'Music: Off':
                Resources.button_sets[name]['current_song'][-1] = True
#        elif name == 'adv_items': # todo
#            Resources.button_sets[name] = {
#                'back' :
#                    [Button, (.1, .85), (.8, .1), 'Back',
#                    Button.adv_back_event, False]
#            } # todo
#        elif name == 'adv_controls': # todo
#            Resources.button_sets[name] = {
#                'p1_left' : [Button, (.1, .4), (.35, .1), 'Player 1 Left: ', Button.pass_event, False],
#                'p1_right' : [Button, (.1, .55), (.35, .1), 'Player 1 Right: ', Button.pass_event, False],
#                'p1_shoot' : [Button, (.1, .7), (.35, .1), 'Player 1 Shoot: ', Button.pass_event, False],
#                'p2_left' : [Button, (.55, .4), (.35, .1), 'Player 2 Left: ', Button.pass_event, False],
#                'p2_right' : [Button, (.55, .55), (.35, .1), 'Player 2 Right: ', Button.pass_event, False],
#                'p2_shoot' : [Button, (.55, .7), (.35, .1), 'Player 2 Shoot: ', Button.pass_event, False],
#                'back' :
#                    [Button, (.1, .85), (.8, .1), 'Back',
#                    Button.adv_back_event, False]
#                #simplegui.KEY_MAP.keys()[simplegui.KEY_MAP.values().index(key)]
#                #'p1_left' : [Button, (.1, .4), (.35, .1), 'Player 1 Left: %s' %s simplegui.KEY_MAP.values(65)]
#            }

    def load_sounds():
        for name, url in Resources.sound_urls.items():
            Resources.sounds[name] = simplegui.load_sound(url)
