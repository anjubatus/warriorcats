from text import *
from random import randint


class Button(object):
    used_screen = screen
    used_mouse = mouse

    def __init__(self, font=verdana, frame_colour=(200, 200, 200), clickable_colour=(150, 150, 150),
                 unavailable_colour=(230, 230, 230)):
        self.text = ''
        self.font = font
        self.frame_colour = frame_colour
        self.clickable_colour = clickable_colour
        self.unavailable_colour = unavailable_colour
        # self.current_colour = self.frame_colour

        # self.available = False   # can button be clicked, even if it's on screen and under mouse?
        # self.clickable = False   # is button available and mouse on top?
        # self.collision = None
        # self.on_screen = False   # is button currently on screen at all?

    def draw_button(self, pos, available=True, image=None, text='', **values):
        # self.on_screen = True

        if not available:
            colour = self.unavailable_colour
        else:
            colour = self.frame_colour

        # creating visible button
        if image is None:
            new_button = pygame.Surface((self.font.text(text) + 10, self.font.size + 6))
        else:
            new_button = image

        new_pos = list(pos)
        if pos[0] == 'center':
            new_pos[0] = screen_x / 2 - new_button.get_width() / 2
        elif pos[0] < 0:
            new_pos[0] = screen_x + pos[0] - new_button.get_width()
        if pos[1] == 'center':
            new_pos[1] = screen_y / 2 - new_button.get_height() / 2
        elif pos[1] < 0:
            new_pos[1] = screen_y + pos[1] - new_button.get_height()

        # Check collision
        collision = self.used_screen.blit(new_button, new_pos)
        clickable = False
        if available and collision.collidepoint(self.used_mouse.pos):
            colour = self.clickable_colour
            clickable = True

        # fill in non-image button
        if image is None:
            new_button.fill(colour)
            self.font.text(text, (5, 0), new_button)
            self.used_screen.blit(new_button, new_pos)
        else:
            self.used_screen.blit(new_button, new_pos)

        # CLICK
        if game.clicked and clickable:
            self.activate(values)

    def check(self):
        """for x in self.all_buttons:
            if x.button_type not in ['writebutton', 'imagebutton']:
                if x.on_screen and not x.available:
                    x.current_colour = x.unavailable_colour
                    x.clickable = False
                elif x.on_screen and x.collision.collidepoint(x.used_mouse.pos):
                    # if mouse howers over button, it will change colour and is clickable
                    x.clickable = True
                    x.current_colour = x.clickable_colour
                else:
                    x.clickable = False
                    x.current_colour = x.frame_colour"""
        pass

    def check_out(self):
        """for x in self.all_buttons:
            x.on_screen = False
            x.available = False"""
        pass

    def activate(self, values=None):
        if values is None:
            values = {}
        for key, value in values.items():
            if key in game.switches.keys():
                game.switches[key] = value
                if key == 'cur_screen':
                    game.all_screens[game.current_screen].screen_switches()
            else:
                print str(key) + ' -key not found...'


"""
class ScreenButton(Button):
    button_type = 'screenbutton'
    # Where a click of the button leads to
    destination = {}

    def init(self, text, destination):
        self.text = text
        self.destination[self] = destination
        self.all_buttons.append(self)

    def activate(self):
        if self.available:
            game.current_screen = self.destination[self]
            game.naming_text = ''
            game.all_screens[game.current_screen].screen_switches()


class SwitchButton(Button):
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


class ImageButton(Button):
    button_type = 'imagebutton'
    images = {}

    def init(self, image, switch_or_screen, dest, value=None):
        self.images[self] = [image, switch_or_screen, dest, value]
        self.all_buttons.append(self)

    def value(self, value):
        self.images[self][3] = value

    def draw_button(self, pos, available=True):
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
"""


class Writer(Button):
    button_type = 'writer'
    abc = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
           'z', 'x', 'c', 'v', 'b', 'n', 'm']
    # abc.sort()
    for i in ['\'', '-', '.']:
        abc.append(i)
    letters = abc
    # letter size is opposite to the current size
    letter_size = 'lower'
    length = 12
    upper = True
    target = 'naming text'

    def init(self, included_letters=None, letters_x=10, target=None):
        if included_letters is not None:
            self.letters = included_letters
        else:
            self.letters = self.abc
        if target is not None:
            self.target = target
        else:
            self.target = 'naming text'

        self.length = letters_x
        # self.collision = {}
        # self.clickable = {}
        # self.current_colour = {}
        self.letter_size = 'lower'
        self.upper = True

        """
        for i in self.letters:
            self.clickable[i] = False
            self.current_colour[i] = self.frame_colour

        self.clickable['lower'] = False
        self.current_colour['lower'] = self.frame_colour
        self.collision['lower'] = screen.blit(pygame.Surface((0, 0)), (0, 0))
        self.clickable['DEL'] = False
        self.current_colour['DEL'] = self.frame_colour"""

    def draw(self, pos, available=True):
        cur_length = 0
        space_y = 0
        space_x = 0
        x = 0
        y = 0

        if self.upper:
            self.letter_size = 'lower'
        else:
            self.letter_size = 'upper'

        # Is writer available?
        if available:
            colour = self.frame_colour
        else:
            colour = self.unavailable_colour

        new_letters = self.letters
        new_letters.append('DEL')
        new_letters.append(self.letter_size)

        for letter in self.letters:
            if self.upper and letter.isalpha():
                new_letter = letter.upper()
            else:
                new_letter = letter
            new_button = pygame.Surface((self.font.text(new_letter) + 10, self.font.size + 6))

            # Check collision
            collision = self.used_screen.blit(new_button, (pos[0] + cur_length + space_x,
                                                           pos[1] + (self.font.size + 6)*y + space_y))
            clickable = False
            if available and collision.collidepoint(self.used_mouse.pos):
                colour = self.clickable_colour
                clickable = True

            # Fill in letter and blit
            new_button.fill(colour)
            self.font.text(new_letter, (5, 0), new_button)
            self.used_screen.blit(new_button, (pos[0] + cur_length + space_x,
                                               pos[1] + (self.font.size + 6)*y + space_y))

            # CLICK
            if game.clicked and clickable:
                self.activate(new_letter)

            # Add pixels for the next letter to follow
            cur_length += self.font.text(new_letter) + 10
            space_x += 2
            x += 1

            if x >= self.length:
                x = 0
                cur_length = 0
                space_x = 0
                space_y += 2
                y += 1

        """for b in [self.letter_size, 'DEL']:
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
                y += 1"""

    def check(self):
        """for i in self.clickable.keys():
            if not self.available:
                self.current_colour[i] = self.unavailable_colour
                self.clickable[i] = False
            elif self.collision[i].collidepoint(self.used_mouse.pos):
                # if mouse howers over button, it will change colour and is clickable
                self.clickable[i] = True
                self.current_colour[i] = self.clickable_colour
            else:
                self.clickable[i] = False
                self.current_colour[i] = self.frame_colour"""
        pass

    def activate(self, values=None):
        if values not in ['upper', 'lower', 'DEL'] and len(game.switches[self.target]) < game.max_name_length\
                and values is not None:
            if self.upper:
                game.switches[self.target] += values.upper()
            else:
                game.switches[self.target] += values
        elif values == 'upper':
            self.upper = True
            self.letter_size = 'lower'
            """self.clickable['lower'] = self.clickable.pop('upper')
            self.collision['lower'] = self.collision.pop('upper')
            self.current_colour['lower'] = self.current_colour.pop('upper')"""
        elif values == 'lower':
            self.upper = False
            self.letter_size = 'upper'
            """self.clickable['upper'] = self.clickable.pop('lower')
            self.collision['upper'] = self.collision.pop('lower')
            self.current_colour['upper'] = self.current_colour.pop('lower')"""
        elif values == 'DEL' and len(game.switches[self.target]) > 0:
            game.switches[self.target] = game.switches[self.target][:-1]


# BUTTONS
buttons = Button()

"""
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
"""

# WRITER
writer = Writer()
writer.init()

"""
# Make example cats
game.cat_buttons = {'cat0': ImageButton(), 'cat1': ImageButton(), 'cat2': ImageButton(), 'cat3': ImageButton(),
                    'cat4': ImageButton(), 'cat5': ImageButton(), 'cat6': ImageButton(), 'cat7': ImageButton(),
                    'cat8': ImageButton(), 'cat9': ImageButton(), 'cat10': ImageButton(), 'cat11': ImageButton()}"""

