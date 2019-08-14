from text import *
from random import randint


class Buttons(object):
    # General buttons parent class
    used_screen = screen
    used_mouse = mouse
    all_buttons = []

    def __init__(self, font=verdana, frame_colour=(200, 200, 200), clickable_colour=(150, 150, 150),
                 unavailable_colour=(230, 230, 230)):
        self.text = ''
        self.font = font
        self.collision = None
        self.frame_colour = frame_colour
        self.clickable_colour = clickable_colour
        self.unavailable_colour = unavailable_colour
        self.current_colour = self.frame_colour
        self.available = False
        self.clickable = False

        self.ID = str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(
                randint(0, 9))
        self.x_screen = None
        self.x_switch = None
        self.x_value = None

    def draw_button(self, pos):
        new_button = pygame.Surface((self.font.text(self.text) + 10, self.font.size + 6))
        new_button.fill(self.current_colour)
        self.font.text(self.text, (5, 0), new_button)

        new_pos = list(pos)
        if pos[0] == 'center':
            new_pos[0] = screen_x / 2 - new_button.get_width() / 2
        elif pos[0] < 0:
            new_pos[0] = screen_x + pos[0] - new_button.get_width()
        if pos[1] == 'center':
            new_pos[1] = screen_y / 2 - new_button.get_height() / 2
        elif pos[1] < 0:
            new_pos[1] = screen_y + pos[1] - new_button.get_height()

        self.used_screen.blit(new_button, new_pos)
        self.collision = self.used_screen.blit(new_button, new_pos)

    def check(self):
        if not self.available:
            self.current_colour = self.unavailable_colour
            self.clickable = False
        elif self.collision.collidepoint(self.used_mouse.pos):
            # if mouse howers over button, it will change colour and is clickable
            self.clickable = True
            self.current_colour = self.clickable_colour
        else:
            self.clickable = False
            self.current_colour = self.frame_colour

    def is_available(self, list_of_available):
        for i in self.all_buttons:
            if i not in list_of_available:
                i.available = False
            else:
                i.available = True

    def activate(self):
        pass


class ScreenButton(Buttons):
    button_type = 'screenbutton'
    # Where a click of the button leads to
    destination = {}

    def init(self, text, destination, switch=None, value=None):
        self.text = text
        self.switch = switch
        self.value = value
        self.destination[self] = [destination, switch, value]
        self.all_buttons.append(self)

    def activate(self):
        if self.available:
            game.current_screen = self.destination[self][0]
            game.naming_text = ''
            game.all_screens[game.current_screen].screen_switches()


class SwitchButton(Buttons):
    button_type = 'switchbutton'
    switches = {}

    def init(self, text, switch, value=None, add=False):  # add is True if value is to be added to a list
        self.text = text
        self.switches[self] = [switch, value, add]
        self.all_buttons.append(self)

    def activate(self):
        if self.available:
            # if value isn't being added to a list
            if not self.switches[self][2]:
                game.switches[self.switches[self][0]] = self.switches[self][1]
            else:
                game.switches[self.switches[self][0]].append(self.switches[self][1])

    def value(self, value):
        self.switches[self][1] = value


class ImageButton(Buttons):
    button_type = 'imagebutton'
    images = {}

    def init(self, image, switch_or_screen, dest, value=None):
        self.images[self] = [image, switch_or_screen, dest, value]
        self.all_buttons.append(self)

    def value(self, value):
        self.images[self][3] = value

    def draw_button(self, pos):
        new_pos = list(pos)
        if pos[0] == 'center':
            new_pos[0] = screen_x / 2 - self.images[self][0].get_size()[0] / 2
        elif pos[0] < 0:
            new_pos[0] = screen_x + pos[0] - self.images[self][0].get_size()[0]
        self.used_screen.blit(self.images[self][0], new_pos)
        self.collision = self.used_screen.blit(self.images[self][0], new_pos)

    def activate(self):
        if self.available:
            if self.images[self][1] == 'switch':
                game.switches[self.images[self][2]] = self.images[self][3]
            elif self.images[self][1] == 'screen':
                game.current_screen = self.images[self][2]
                game.naming_text = ''
                game.all_screens[game.current_screen].screen_switches()


class WriteButton(Buttons):
    button_type = 'writebutton'
    abc = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
           'z', 'x', 'c', 'v', 'b', 'n', 'm']
    abc.sort()
    for i in ['\'', '-', '.']:
        abc.append(i)
    letters = abc
    # letter size is opposite to the current size
    letter_size = 'lower'
    length = 12
    upper = True

    def init(self, included_letters=None, letters_x=12):
        # this function isn't necessary, unless you want to change defaults
        if included_letters is not None:
            self.letters = included_letters
        self.length = letters_x
        self.collision = {}
        self.clickable = {}
        self.current_colour = {}
        self.letter_size = 'lower'
        self.upper = True

        for i in self.letters:
            self.clickable[i] = False
            self.current_colour[i] = self.frame_colour

        self.clickable['lower'] = False
        self.current_colour['lower'] = self.frame_colour
        self.collision['lower'] = screen.blit(pygame.Surface((0, 0)), (0, 0))
        self.clickable['DEL'] = False
        self.current_colour['DEL'] = self.frame_colour

        self.all_buttons.append(self)

    def draw_button(self, pos):
        cur_length = 0
        space_y = 0
        space_x = 0
        x = 0
        y = 0
        for z in self.letters:
            if self.upper and z.isalpha():
                new_z = z.upper()
            else:
                new_z = z
            new_button = pygame.Surface((self.font.text(new_z) + 10, self.font.size + 6))
            new_button.fill(self.current_colour[z])
            self.font.text(new_z, (5, 0), new_button)
            self.used_screen.blit(new_button, (pos[0] + cur_length + space_x,
                                               pos[1] + (self.font.size + 6)*y + space_y))
            self.collision[z] = self.used_screen.blit(new_button, (pos[0] + cur_length + space_x,
                                                                   pos[1] + (self.font.size + 6)*y + space_y))

            cur_length += self.font.text(new_z) + 10
            space_x += 2
            x += 1

            if x >= self.length:
                x = 0
                cur_length = 0
                space_x = 0
                space_y += 2
                y += 1

        for b in [self.letter_size, 'DEL']:
            new_button = pygame.Surface((self.font.text(b) + 10, self.font.size + 6))
            new_button.fill(self.current_colour[b])
            self.font.text(b, (5, 0), new_button)
            self.used_screen.blit(new_button, (pos[0] + cur_length + space_x,
                                               pos[1] + (self.font.size + 6) * y + space_y))
            self.collision[b] = self.used_screen.blit(new_button, (pos[0] + cur_length + space_x,
                                                                   pos[1] + (self.font.size + 6) * y + space_y))

            cur_length += self.font.text(b) + 10
            space_x += 2
            x += 1

            if x >= self.length:
                x = 0
                cur_length = 0
                space_x = 0
                space_y += 2
                y += 1

    def check(self):
        if self.upper:
            self.letter_size = 'lower'
        else:
            self.letter_size = 'upper'

        for i in self.clickable.keys():
            if not self.available:
                self.current_colour[i] = self.unavailable_colour
                self.clickable[i] = False
            elif self.collision[i].collidepoint(self.used_mouse.pos):
                # if mouse howers over button, it will change colour and is clickable
                self.clickable[i] = True
                self.current_colour[i] = self.clickable_colour
            else:
                self.clickable[i] = False
                self.current_colour[i] = self.frame_colour

    def activate(self):
        if self.available:
            for i in self.clickable.keys():
                if self.clickable[i]:
                    if i not in ['upper', 'lower', 'DEL'] and len(game.naming_text) < game.max_name_length:
                        if self.upper:
                            game.naming_text += i.upper()
                        else:
                            game.naming_text += i
                    elif i == 'upper':
                        self.upper = True
                        self.letter_size = 'lower'
                        self.clickable['lower'] = self.clickable.pop('upper')
                        self.collision['lower'] = self.collision.pop('upper')
                        self.current_colour['lower'] = self.current_colour.pop('upper')
                    elif i == 'lower':
                        self.upper = False
                        self.letter_size = 'upper'
                        self.clickable['upper'] = self.clickable.pop('lower')
                        self.collision['upper'] = self.collision.pop('lower')
                        self.current_colour['upper'] = self.current_colour.pop('lower')
                    elif i == 'DEL' and len(game.naming_text) > 0:
                        game.naming_text = game.naming_text[:-1]


# BUTTONS
# Create the buttons here; in the screens file first activate all the buttons neede on the specific screen,
# draw the button, then check().
buttons = Buttons()

# screen buttons
screen_buttons = {'continue': ['Continue >', 'clan screen'],
                  'back to main': ['< Back To Main Menu', 'start screen'], 'make new': ['Make New >', 'make clan screen'],
                  'clan created': ['Done', 'clan created screen'], 'events': ['EVENTS', 'events screen'],
                  'clan': ['CLAN', 'clan screen'], 'event': ['Complete', 'single event screen']}

for x in screen_buttons.keys():
    a = screen_buttons[x][0]
    b = screen_buttons[x][1]
    screen_buttons[x] = ScreenButton()
    screen_buttons[x].init(a, b)


# Switch buttons
# To complete some switch buttons, add the final value in the main file in update_switches
switch_buttons = {'clan name': ['Choose this name!', 'clan name'], 'leader': ['Bless this cat with 9 lives', 'leader'],
                  'medicine cat': ['This cat will take care of the clan', 'medicine cat'],
                  'members': ['Recruit this cat to your clan', 'members', True]}
for z in switch_buttons.keys():
    if len(switch_buttons[z]) > 2:
        a = switch_buttons[z][0]
        b = switch_buttons[z][1]
        c = switch_buttons[z][2]
        switch_buttons[z] = SwitchButton()
        switch_buttons[z].init(a, b, add=c)
    else:
        a = switch_buttons[z][0]
        b = switch_buttons[z][1]
        switch_buttons[z] = SwitchButton()
        switch_buttons[z].init(a, b)


# WRITER
writer = WriteButton()
writer.init()


# Make example cats
game.cat_buttons = {'cat0': ImageButton(), 'cat1': ImageButton(), 'cat2': ImageButton(), 'cat3': ImageButton(),
                    'cat4': ImageButton(), 'cat5': ImageButton(), 'cat6': ImageButton(), 'cat7': ImageButton(),
                    'cat8': ImageButton(), 'cat9': ImageButton(), 'cat10': ImageButton(), 'cat11': ImageButton()}

