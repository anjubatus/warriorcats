import pygame

screen_x = 800
screen_y = 700
screen = pygame.display.set_mode((screen_x, screen_y), pygame.HWSURFACE)
pygame.display.set_caption('Warrior Cats Simulator')


# G A M E
class Game(object):
    # random items to be used
    new_born = False
    naming_box = pygame.Surface((100, 20))
    naming_box.fill((230, 230, 230))
    naming_text = ''
    max_name_length = 8
    choose_cats = {}
    cat_buttons = {'cat0': None, 'cat1': None, 'cat2': None, 'cat3': None,
                   'cat4': None, 'cat5': None, 'cat6': None, 'cat7': None,
                   'cat8': None, 'cat9': None, 'cat10': None, 'cat11': None}

    switches = {'cat': None, 'clan name': None, 'leader': None, 'medicine cat': None, 'members': [],
                'event': None}
    all_screens = {}

    cur_events = {}

    # CLAN
    clan = None

    def __init__(self, current_screen='start screen'):
        self.current_screen = current_screen


# M O U S E
class Mouse(object):
    used_screen = screen

    def __init__(self):
        self.pos = (0, 0)

    def check_pos(self):
        self.pos = pygame.mouse.get_pos()


mouse = Mouse()
game = Game()
