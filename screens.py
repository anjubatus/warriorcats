from clan import *
from events import *


# SCREENS PARENT CLASS
class Screens(object):
    game_screen = screen
    game_x = screen_x
    game_y = screen_y
    all_screens = {}

    def __init__(self, name=None):
        self.name = name
        if name is not None:
            self.all_screens[name] = self
            game.all_screens[name] = self

    def on_use(self):
        pass

    def screen_switches(self):
        pass


# SCREEN CHILD CLASSES
class StartScreen(Screens):
    def on_use(self):
        # check available buttons
        if game.clan is not None:
            buttons.is_available([screen_buttons['continue'], screen_buttons['make new']])
        else:
            buttons.is_available([screen_buttons['make new']])

        # layout
        verdana.text('Welcome to CLAN SIMULATOR.', ('center', 100))
        example_cat.draw_big((350, 150))

        screen_buttons['continue'].draw_button(('center', 300))
        screen_buttons['continue'].check()
        screen_buttons['make new'].draw_button(('center', 350))
        screen_buttons['make new'].check()

    def screen_switches(self):
        if game.clan is not None:
            for x in cat_class.all_cats.keys():
                if x not in game.clan.clan_cats:
                    game.clan.remove_cat(x)


class ClanScreen(Screens):
    all_buttons = []

    def on_use(self):
        if game.switches['cat'] is not None:
            game.current_screen = 'profile screen'
        # check available buttons
        buttons.is_available(self.all_buttons)

        # layout
        verdana_big.text(game.clan.name + 'Clan', ('center', 30))
        verdana.text('Leader\'s Den', game.clan.cur_layout['leader den'])
        verdana.text('Medicine Cat Den', game.clan.cur_layout['medicine den'])
        verdana.text('Nursery', game.clan.cur_layout['nursery'])
        verdana.text('Clearing', game.clan.cur_layout['clearing'])
        verdana.text('Apprentices\' Den', game.clan.cur_layout['apprentice den'])
        verdana.text('Warriors\' Den', game.clan.cur_layout['warrior den'])
        verdana.text('Elders\' Den', game.clan.cur_layout['elder den'])

        for x in game.clan.clan_cats:
            # print x, cat_class.all_cats[x].placement
            game.cat_buttons[x].draw_button(cat_class.all_cats[x].placement)
            game.cat_buttons[x].check()

        screen_buttons['events'].draw_button((330, 70))
        screen_buttons['events'].check()
        screen_buttons['clan'].draw_button((410, 70))
        screen_buttons['clan'].check()
        screen_buttons['back to main'].draw_button((50, 50))
        screen_buttons['back to main'].check()

    def screen_switches(self):
        cat_profiles()
        self.all_buttons.append(screen_buttons['back to main'])
        self.all_buttons.append(screen_buttons['events'])
        for a in game.cat_buttons.values():
            self.all_buttons.append(a)
        game.switches['cat'] = None

        p = game.clan.cur_layout
        game.clan.leader.placement = choice(p['leader place'])
        game.clan.medicine_cat.placement = choice(p['medicine place'])

        # print 'SECOND SCREEN SWITCH, GAME.CLAN.CLAN_CATS:'
        # print game.clan.clan_cats
        for x in game.clan.clan_cats:
            if cat_class.all_cats[x].status == 'warrior':
                cat_class.all_cats[x].placement = choice([choice(p['warrior place']), choice(p['clearing place'])])
            elif cat_class.all_cats[x].status == 'kitten':
                cat_class.all_cats[x].placement = choice(p['nursery place'])
            elif cat_class.all_cats[x].status == 'elder':
                cat_class.all_cats[x].placement = choice(p['elder place'])
            elif cat_class.all_cats[x].status == 'apprentice':
                cat_class.all_cats[x].placement = choice([choice(p['apprentice place']), choice(p['clearing place'])])


class MakeClanScreen(Screens):
    def first_phase(self):
        # check available buttons
        buttons.is_available([screen_buttons['back to main'], writer, switch_buttons['clan name']])

        # layout
        verdana.text('NAME YOUR CLAN!', ('center', 150))
        self.game_screen.blit(game.naming_box, (330, 200))
        verdana.text(game.naming_text, (335, 200))
        verdana.text('-Clan', (440, 200))
        verdana.text('Max eight letters long. Don\'t include "Clan" in it.', ('center', 250))

        screen_buttons['back to main'].draw_button((50, 50))
        screen_buttons['back to main'].check()

        writer.draw_button((250, 300))
        writer.check()

        switch_buttons['clan name'].draw_button(('center', 500))
        switch_buttons['clan name'].check()

    def second_phase(self):
        # check available buttons
        buttons.is_available([screen_buttons['back to main'], game.cat_buttons['cat0'], game.cat_buttons['cat1'],
                              game.cat_buttons['cat2'], game.cat_buttons['cat3'], game.cat_buttons['cat4'],
                              game.cat_buttons['cat5'], game.cat_buttons['cat6'], game.cat_buttons['cat7'],
                              game.cat_buttons['cat8'], game.cat_buttons['cat9'], game.cat_buttons['cat10'],
                              game.cat_buttons['cat11'], switch_buttons['leader']])

        # LAYOUT
        verdana.text(game.switches['clan name']+'Clan', ('center', 50))
        verdana.text('These twelve cats are your potential clan members.', ('center', 100))
        verdana.text('First, pick your leader from them:', ('center', 150))

        # cat buttons / small sprites
        for u in range(6):
            game.cat_buttons['cat' + str(u)].draw_button((50, 150 + 50*u))
            game.cat_buttons['cat' + str(u)].check()
        for u in range(6, 12):
            game.cat_buttons['cat' + str(u)].draw_button((screen_x - 100, 150 + 50*(u-6)))
            game.cat_buttons['cat' + str(u)].check()

        # cat profiles
        if 12 > game.switches['cat'] >= 0:
            game.choose_cats[game.switches['cat']].draw_large((320, 200))
            verdana.text(str(game.choose_cats[game.switches['cat']].name) + ' --> ' +
                             game.choose_cats[game.switches['cat']].name.prefix + 'star', ('center', 360))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].gender), (330, 385))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].age), (330, 405))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].trait), (330, 425))

            if game.choose_cats[game.switches['cat']].age in ['kitten', 'adolescent']:
                verdana_red.text('Too young to become leader.', (300, 490))
            else:
                switch_buttons['leader'].draw_button(('center', 490))
                switch_buttons['leader'].check()

        screen_buttons['back to main'].draw_button((50, 50))
        screen_buttons['back to main'].check()

    def third_phase(self):
        # check available buttons
        buttons.is_available([screen_buttons['back to main'], game.cat_buttons['cat0'], game.cat_buttons['cat1'],
                              game.cat_buttons['cat2'], game.cat_buttons['cat3'], game.cat_buttons['cat4'],
                              game.cat_buttons['cat5'], game.cat_buttons['cat6'], game.cat_buttons['cat7'],
                              game.cat_buttons['cat8'], game.cat_buttons['cat9'], game.cat_buttons['cat10'],
                              game.cat_buttons['cat11'], switch_buttons['medicine cat']])

        # LAYOUT
        verdana.text(game.switches['clan name'] + 'Clan', ('center', 50))
        verdana.text('Second, pick your medicine cat:', ('center', 100))

        # cat buttons / small sprites
        for u in range(6):
            if game.switches['leader'] == game.choose_cats[u]:
                game.choose_cats[u].draw((screen_x/2 - 25, 550))
            else:
                game.cat_buttons['cat' + str(u)].draw_button((50, 150 + 50*u))
                game.cat_buttons['cat' + str(u)].check()
        for u in range(6, 12):
            if game.switches['leader'] == game.choose_cats[u]:
                game.choose_cats[u].draw((screen_x/2 - 25, 550))
            else:
                game.cat_buttons['cat' + str(u)].draw_button((screen_x - 100, 150 + 50*(u-6)))
                game.cat_buttons['cat' + str(u)].check()

        # cat profiles
        if 12 > game.switches['cat'] >= 0 and game.choose_cats[game.switches['cat']] != game.switches['leader']:
            game.choose_cats[game.switches['cat']].draw_large((320, 200))
            verdana.text(str(game.choose_cats[game.switches['cat']].name), ('center', 360))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].gender), (330, 385))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].age), (330, 405))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].trait), (330, 425))

            if game.choose_cats[game.switches['cat']].age in ['kitten', 'adolescent']:
                verdana_red.text('Too young to become medicine cat.', (300, 490))
            else:
                switch_buttons['medicine cat'].draw_button(('center', 490))
                switch_buttons['medicine cat'].check()

        screen_buttons['back to main'].draw_button((50, 50))
        screen_buttons['back to main'].check()

    def fourth_phase(self):
        # check available buttons
        if len(game.switches['members']) < 4:
            buttons.is_available([screen_buttons['back to main'], game.cat_buttons['cat0'], game.cat_buttons['cat1'],
                                  game.cat_buttons['cat2'], game.cat_buttons['cat3'], game.cat_buttons['cat4'],
                                  game.cat_buttons['cat5'], game.cat_buttons['cat6'], game.cat_buttons['cat7'],
                                  game.cat_buttons['cat8'], game.cat_buttons['cat9'], game.cat_buttons['cat10'],
                                  game.cat_buttons['cat11'], switch_buttons['members']])
        else:
            buttons.is_available([screen_buttons['back to main'], game.cat_buttons['cat0'], game.cat_buttons['cat1'],
                                  game.cat_buttons['cat2'], game.cat_buttons['cat3'], game.cat_buttons['cat4'],
                                  game.cat_buttons['cat5'], game.cat_buttons['cat6'], game.cat_buttons['cat7'],
                                  game.cat_buttons['cat8'], game.cat_buttons['cat9'], game.cat_buttons['cat10'],
                                  game.cat_buttons['cat11'], switch_buttons['members'], screen_buttons['clan created']])

        # LAYOUT
        verdana.text(game.switches['clan name'] + 'Clan', ('center', 50))
        verdana.text('Finally, recruit from 4 to 7 more members to your clan.', ('center', 100))
        verdana.text('Choose wisely...', ('center', 150))

        # cat buttons / small sprites
        for u in range(6):
            if game.switches['leader'] == game.choose_cats[u]:
                game.choose_cats[u].draw((screen_x / 2 - 50, 550))
            elif game.switches['medicine cat'] == game.choose_cats[u]:
                game.choose_cats[u].draw((screen_x / 2, 550))
            elif game.choose_cats[u] in game.switches['members']:
                game.choose_cats[u].draw((screen_x / 2 - 50*(u+2), 550))
            else:
                game.cat_buttons['cat' + str(u)].draw_button((50, 150 + 50 * u))
                game.cat_buttons['cat' + str(u)].check()
        for u in range(6, 12):
            if game.switches['leader'] == game.choose_cats[u]:
                game.choose_cats[u].draw((screen_x / 2 - 50, 550))
            elif game.switches['medicine cat'] == game.choose_cats[u]:
                game.choose_cats[u].draw((screen_x / 2, 550))
            elif game.choose_cats[u] in game.switches['members']:
                game.choose_cats[u].draw((screen_x / 2 + 50*(u-5), 550))
            else:
                game.cat_buttons['cat' + str(u)].draw_button((screen_x - 100, 150 + 50 * (u - 6)))
                game.cat_buttons['cat' + str(u)].check()

        # cat profiles
        if 12 > game.switches['cat'] >= 0 and \
                game.choose_cats[game.switches['cat']] not in [game.switches['leader'], game.switches['medicine cat']]\
                and game.choose_cats[game.switches['cat']] not in game.switches['members']:
            game.choose_cats[game.switches['cat']].draw_large((320, 200))
            verdana.text(str(game.choose_cats[game.switches['cat']].name), ('center', 360))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].gender), (330, 385))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].age), (330, 405))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].trait), (330, 425))

            if len(game.switches['members']) < 7:
                switch_buttons['members'].draw_button(('center', 490))
                switch_buttons['members'].check()
        screen_buttons['clan created'].draw_button(('center', 630))
        screen_buttons['clan created'].check()

        screen_buttons['back to main'].draw_button((50, 50))
        screen_buttons['back to main'].check()

    def on_use(self):
        if len(game.switches['clan name']) == 0:
            self.first_phase()
        elif len(game.switches['clan name']) > 0 and game.switches['leader'] is None:
            self.second_phase()
        elif game.switches['leader'] is not None and game.switches['medicine cat'] is None:
            self.third_phase()
        else:
            self.fourth_phase()

    def screen_switches(self):
        game.cat_buttons = {'cat0': ImageButton(), 'cat1': ImageButton(), 'cat2': ImageButton(), 'cat3': ImageButton(),
                            'cat4': ImageButton(), 'cat5': ImageButton(), 'cat6': ImageButton(), 'cat7': ImageButton(),
                            'cat8': ImageButton(), 'cat9': ImageButton(), 'cat10': ImageButton(),
                            'cat11': ImageButton()}

        game.switches['clan name'] = ''
        game.switches['leader'] = None
        game.switches['cat'] = None
        game.switches['medicine cat'] = None
        game.switches['members'] = []
        example_cats()


class ClanCreatedScreen(Screens):
    def on_use(self):
        # available buttons
        buttons.is_available([screen_buttons['continue']])

        # LAYOUT
        verdana.text('Your clan has been created!', ('center', 50))
        game.switches['leader'].draw_big((screen_x/2 - 50, 100))

        screen_buttons['continue'].draw_button(('center', 250))
        screen_buttons['continue'].check()

    def screen_switches(self):
        game.clan = Clan(game.switches['clan name'], game.switches['leader'], game.switches['medicine cat'])
        # print 'members:'
        # print game.switches['members']
        # print 'all cats:'
        # print cat_class.all_cats.values()
        for i in cat_class.all_cats.values():
            if i in game.switches['members']:
                game.clan.add_cat(i)
            elif i != game.switches['leader'] and i != game.switches['medicine cat']:
                game.clan.remove_cat(i.ID)
        cat_class.save_cats()
        game.clan.save_clan()

        # print
        # print game.cat_buttons.keys()
        # print
        # print cat_class.all_cats.keys()


class EventsScreen(Screens):
    def on_use(self):
        # available buttons
        buttons.is_available([screen_buttons['back to main'], screen_buttons['clan'], screen_buttons['event']])

        # LAYOUT
        verdana_big.text(game.clan.name + 'Clan', ('center', 30))
        verdana.text('Check this page to see which events are currently happening at the clan.', ('center', 100))

        a = 0
        if len(game.cur_events) > 0:
            for x in game.cur_events.keys():
                events_class.all_events[x].news(('center', 150 + a))
                screen_buttons['event'].draw_button(('center', 200 + a))
                screen_buttons['event'].check()
                a += 150

        screen_buttons['events'].draw_button((330, 70))
        screen_buttons['events'].check()
        screen_buttons['clan'].draw_button((410, 70))
        screen_buttons['clan'].check()
        screen_buttons['back to main'].draw_button((50, 50))
        screen_buttons['back to main'].check()


class ProfileScreen(Screens):
    def on_use(self):
        # available buttons
        buttons.is_available([screen_buttons['continue']])

        # LAYOUT
        verdana.text('PROFILE HERE', ('center', 70))
        cat_class.all_cats[game.switches['cat']].draw_large(('center', 100))
        verdana.text(str(cat_class.all_cats[game.switches['cat']].name), ('center', 300))
        verdana_small.text(cat_class.all_cats[game.switches['cat']].gender, ('center', 330))
        verdana_small.text(cat_class.all_cats[game.switches['cat']].status, ('center', 345))
        verdana_small.text(cat_class.all_cats[game.switches['cat']].age, ('center', 360))
        verdana_small.text(cat_class.all_cats[game.switches['cat']].trait, ('center', 375))
        verdana_small.text(cat_class.all_cats[game.switches['cat']].skill, ('center', 390))
        verdana_small.text('eyes: ' + cat_class.all_cats[game.switches['cat']].eye_colour.lower(), ('center', 405))
        verdana_small.text('pelt: ' + cat_class.all_cats[game.switches['cat']].pelt.name.lower(), ('center', 420))
        verdana_small.text('fur length: ' + cat_class.all_cats[game.switches['cat']].pelt.length, ('center', 435))

        screen_buttons['continue'].draw_button(('center', -150))
        screen_buttons['continue'].check()


class SingleEventScreen(Screens):
    def on_use(self):
        buttons.is_available([screen_buttons['continue']])

        # LAYOUT
        if game.switches['event'] is not None:
            events_class.all_events[game.switches['event']].page()

        screen_buttons['continue'].draw_button(('center', 500))
        screen_buttons['continue'].check()

    def screen_switches(self):
        pass


# SCREENS
screens = Screens()

start_screen = StartScreen('start screen')
clan_screen = ClanScreen('clan screen')
make_clan_screen = MakeClanScreen('make clan screen')
clan_created_screen = ClanCreatedScreen('clan created screen')
events_screen = EventsScreen('events screen')
profile_screen = ProfileScreen('profile screen')
single_event_screen = SingleEventScreen('single event screen')


# CAT PROFILES
def cat_profiles():
    game.choose_cats.clear()
    game.cat_buttons.clear()
    for x in game.clan.clan_cats:
        game.choose_cats[x] = cat_class.all_cats[x]
        game.choose_cats[x].update_sprite()
        game.cat_buttons[x] = ImageButton()
        game.cat_buttons[x].init(game.choose_cats[x].sprite, 'switch', 'cat', x)
