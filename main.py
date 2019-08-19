# Make cats and start clans with them
from screens import *
import sys


# P Y G A M E
clock = pygame.time.Clock()


# update switch values
def update_switches():
    switch_buttons['clan name'].value(game.switches['naming text'])
    if game.switches['cat'] is not None and game.switches['cat'] in game.choose_cats.keys():
        switch_buttons['leader'].value(game.choose_cats[game.switches['cat']])
        switch_buttons['medicine cat'].value(game.choose_cats[game.switches['cat']])
        switch_buttons['members'].value(game.choose_cats[game.switches['cat']])

    if game.clan is not None:
        greencough.init()
        leader_cer.init(game.clan.leader)


events_class.day()


# load cats & clan
with open('saves/cats.txt', 'r') as read_file:
    if_cats = len(read_file.read())
if if_cats > 0:
    cat_class.load_cats()
    clan_class.load_clan()

while True:
    screen.fill((255, 255, 255))
    mouse.check_pos()

    # SCREENS
    game.all_screens[game.current_screen].on_use()

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            # close pygame
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print cat_class.all_cats

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()

        # MOUSE CLICK
        if event.type == pygame.MOUSEBUTTONDOWN:
            for x in buttons.all_buttons:
                if x.collision is not None:
                    x.check()
                if x.button_type != 'writebutton':
                    if x.clickable:
                        print 'clicking...'
                        # updating switches
                        update_switches()

                        # activating button
                        x.activate()
                else:
                    # WRITER/KEYBOARD
                    for a in x.clickable.keys():
                        if x.clickable[a]:
                            x.activate()

    # END FRAME
    buttons.check_out()
    clock.tick(60)

    pygame.display.update()
