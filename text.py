from game_essentials import *
pygame.init()


class Font(object):
    used_screen = screen

    def __init__(self, name, size=15, colour=(0, 0, 0)):
        self.name = name
        self.size = size
        self.colour = colour
        self.font = pygame.font.SysFont(name, size)

    def text(self, text, pos=None, where=used_screen):
        t = self.font.render(text, 1, self.colour)
        if pos is not None:
            # setting on or both items in tuple to 'center' centers the text to the screen.
            # negative pos value will be taken from the other end of the screen
            new_pos = list(pos)
            if pos[0] == 'center':
                new_pos[0] = screen_x/2 - t.get_width()/2
            elif pos[0] < 0:
                new_pos[0] = screen_x + pos[0] - t.get_width()
            if pos[1] == 'center':
                new_pos[1] = screen_y/2 - t.get_height()/2
            elif pos[1] < 0:
                new_pos[1] = screen_y + pos[1] - t.get_height()
            where.blit(t, new_pos)
        # returns length, if assigned to a variable
        return t.get_width()


# F O N T S
verdana = Font('verdana')
verdana_red = Font('verdana', colour=(242, 52, 29))
verdana_small = Font('verdana', 11)
verdana_baby = Font('verdana', 11, (100, 100, 250))
verdana_big = Font('verdana', 18)
