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
        # layout
        verdana.text('Welcome to CLAN GENERATOR.', ('center', 100))
        example_cat.draw_big((350, 150))

        # buttons
        if game.clan is not None:
            buttons.draw_button(('center', 300), text='Continue >', cur_screen='clan screen')
        else:
            buttons.draw_button(('center', 300), text='Continue >', available=False)
        buttons.draw_button(('center', 350), text='Make New >', cur_screen='make clan screen')

    def screen_switches(self):
        if game.clan is not None:
            for x in cat_class.all_cats.keys():
                if x not in game.clan.clan_cats:
                    game.clan.remove_cat(x)


class ClanScreen(Screens):
    def on_use(self):
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
            buttons.draw_button(cat_class.all_cats[x].placement, image=cat_class.all_cats[x].sprite, cat=x,
                                cur_screen='profile screen')

        # buttons
        buttons.draw_button((330, 70), text='EVENTS', cur_screen='events screen')
        buttons.draw_button((410, 70), text='CLAN', available=False)
        buttons.draw_button((50, 50), text='< Back to Main Menu', cur_screen='start screen')

    def screen_switches(self):
        cat_profiles()
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
        # layout
        verdana.text('NAME YOUR CLAN!', ('center', 150))
        self.game_screen.blit(game.naming_box, (330, 200))
        verdana.text(game.switches['naming_text'], (335, 200))
        verdana.text('-Clan', (440, 200))
        verdana.text('Max eight letters long. Don\'t include "Clan" in it.', ('center', 250))

        # buttons
        verdana_small.text('Note: going back to main menu resets the new generated cats.', (50, 25))
        buttons.draw_button((50, 50), text='<< Back to Main Menu', cur_screen='start screen', naming_text='')
        writer.draw((290, 300))
        buttons.draw_button(('center', 500), text='Name Clan', clan_name=game.switches['naming_text'])

    def second_phase(self):
        # LAYOUT
        verdana.text(game.switches['clan_name']+'Clan', ('center', 90))
        verdana.text('These twelve cats are your potential clan members.', ('center', 120))
        verdana.text('First, pick your leader from them:', ('center', 150))

        # cat buttons / small sprites
        for u in range(6):
            buttons.draw_button((50, 150 + 50*u), image=game.choose_cats[u].sprite,
                                cat=u)
        for u in range(6, 12):
            buttons.draw_button((screen_x - 100, 150 + 50*(u-6)), image=game.choose_cats[u].sprite,
                                cat=u)

        # cat profiles
        if 12 > game.switches['cat'] >= 0:
            game.choose_cats[game.switches['cat']].draw_large((320, 200))
            verdana.text(str(game.choose_cats[game.switches['cat']].name) + ' --> ' +
                             game.choose_cats[game.switches['cat']].name.prefix + 'star', ('center', 360))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].gender), (330, 385))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].age), (330, 405))
            if game.choose_cats[game.switches['cat']].age == 'kitten':
                verdana_baby.text(str(game.choose_cats[game.switches['cat']].trait), (330, 425))
            else:
                verdana_small.text(str(game.choose_cats[game.switches['cat']].trait), (330, 425))

            if game.choose_cats[game.switches['cat']].age in ['kitten', 'adolescent']:
                verdana_red.text('Too young to become leader.', (300, 490))
            else:
                buttons.draw_button(('center', 490), text='Grant this cat their nine lives',
                                    leader=game.switches['cat'])

        # buttons
        verdana_small.text('Note: going back to main menu resets the new generated cats.', (50, 25))
        buttons.draw_button((50, 50), text='<< Back to Main Menu', cur_screen='start screen', naming_text='')
        buttons.draw_button((-50, 50), text='< Last step', clan_name='', cat=None)

    def third_phase(self):
        # LAYOUT
        verdana.text(game.switches['clan_name'] + 'Clan', ('center', 90))
        verdana.text('Second, pick your medicine cat:', ('center', 120))

        # cat buttons / small sprites
        for u in range(6):
            if game.switches['leader'] == u:
                game.choose_cats[u].draw((screen_x/2 - 25, 550))
            else:
                buttons.draw_button((50, 150 + 50 * u), image=game.choose_cats[u].sprite,
                                    cat=u)
        for u in range(6, 12):
            if game.switches['leader'] == u:
                game.choose_cats[u].draw((screen_x/2 - 25, 550))
            else:
                buttons.draw_button((screen_x - 100, 150 + 50 * (u - 6)), image=game.choose_cats[u].sprite,
                                    cat=u)

        # cat profiles
        if 12 > game.switches['cat'] >= 0 and game.switches['cat'] != game.switches['leader']:
            game.choose_cats[game.switches['cat']].draw_large((320, 200))
            verdana.text(str(game.choose_cats[game.switches['cat']].name), ('center', 360))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].gender), (330, 385))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].age), (330, 405))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].trait), (330, 425))

            if game.choose_cats[game.switches['cat']].age == 'kitten':
                verdana_red.text('Too young to become medicine cat.', (300, 490))
            else:
                buttons.draw_button(('center', 490), text='This cat will take care of the clan',
                                    medicine_cat=game.switches['cat'])

        # buttons
        verdana_small.text('Note: going back to main menu resets the new generated cats.', (50, 25))
        buttons.draw_button((50, 50), text='<< Back to Main Menu', cur_screen='start screen', naming_text='')
        buttons.draw_button((-50, 50), text='< Last step', leader=None, cat=None)

    def fourth_phase(self):
        # LAYOUT
        verdana.text(game.switches['clan_name'] + 'Clan', ('center', 90))
        verdana.text('Finally, recruit from 4 to 7 more members to your clan.', ('center', 120))
        verdana.text('Choose wisely...', ('center', 150))

        # cat buttons / small sprites
        for u in range(6):
            if game.switches['leader'] == u:
                game.choose_cats[u].draw((screen_x / 2 - 50, 550))
            elif game.switches['medicine_cat'] == u:
                game.choose_cats[u].draw((screen_x / 2, 550))
            elif u in game.switches['members']:
                game.choose_cats[u].draw((screen_x / 2 - 50*(u+2), 550))
            else:
                buttons.draw_button((50, 150 + 50 * u), image=game.choose_cats[u].sprite,
                                    cat=u)
        for u in range(6, 12):
            if game.switches['leader'] == u:
                game.choose_cats[u].draw((screen_x / 2 - 50, 550))
            elif game.switches['medicine_cat'] == u:
                game.choose_cats[u].draw((screen_x / 2, 550))
            elif u in game.switches['members']:
                game.choose_cats[u].draw((screen_x / 2 + 50*(u-5), 550))
            else:
                buttons.draw_button((screen_x - 100, 150 + 50 * (u - 6)), image=game.choose_cats[u].sprite,
                                    cat=u)

        # cat profiles
        if 12 > game.switches['cat'] >= 0 and \
                game.switches['cat'] not in [game.switches['leader'], game.switches['medicine_cat']]\
                and game.switches['cat'] not in game.switches['members']:
            game.choose_cats[game.switches['cat']].draw_large((320, 200))
            verdana.text(str(game.choose_cats[game.switches['cat']].name), ('center', 360))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].gender), (330, 385))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].age), (330, 405))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].trait), (330, 425))

            if len(game.switches['members']) < 7:
                buttons.draw_button(('center', 490), text='Recruit', members=game.switches['cat'], add=True)

        verdana_small.text('Note: clicking Done erases any former clan you may have made from memory.', ('center', 660))

        # buttons
        verdana_small.text('Note: going back to main menu resets the new generated cats.', (50, 25))
        buttons.draw_button((50, 50), text='<< Back to Main Menu', cur_screen='start screen', naming_text='')
        buttons.draw_button((-50, 50), text='< Last step', medicine_cat=None, members=[], cat=None)
        if len(game.switches['members']) > 3:
            buttons.draw_button(('center', 630), text='Done', cur_screen='clan created screen')
        else:
            buttons.draw_button(('center', 630), text='Done', available=False)

    def on_use(self):
        if len(game.switches['clan_name']) == 0:
            self.first_phase()
        elif len(game.switches['clan_name']) > 0 and game.switches['leader'] is None:
            self.second_phase()
        elif game.switches['leader'] is not None and game.switches['medicine_cat'] is None:
            self.third_phase()
        else:
            self.fourth_phase()

    def screen_switches(self):
        game.switches['clan_name'] = ''
        writer.upper = True
        game.switches['leader'] = None
        game.switches['cat'] = None
        game.switches['medicine_cat'] = None
        game.switches['members'] = []
        example_cats()


class ClanCreatedScreen(Screens):
    def on_use(self):
        # LAYOUT
        verdana.text('Your clan has been created!', ('center', 50))
        game.clan.leader.draw_big((screen_x/2 - 50, 100))

        # buttons
        buttons.draw_button(('center', 250), text='Continue', cur_screen='clan screen')

    def screen_switches(self):
        game.clan = Clan(game.switches['clan_name'], game.choose_cats[game.switches['leader']],
                         game.choose_cats[game.switches['medicine_cat']])
        for i in cat_class.all_cats.values():
            not_found = True
            for x in game.switches['members']:
                if i == game.choose_cats[x]:
                    game.clan.add_cat(i)
                    not_found = False
            if i != game.choose_cats[game.switches['leader']] and i != game.choose_cats[game.switches['medicine_cat']]\
                    and not_found:
                game.clan.remove_cat(i.ID)
        cat_class.save_cats()
        game.clan.save_clan()


class EventsScreen(Screens):
    def on_use(self):
        # LAYOUT
        verdana_big.text(game.clan.name + 'Clan', ('center', 30))
        verdana.text('Check this page to see which events are currently happening at the clan.', ('center', 100))

        a = 0
        """if len(game.cur_events) > 0:
            for x in game.cur_events.keys():
                events_class.all_events[x].news(('center', 150 + a))
                screen_buttons['event'].draw_button(('center', 200 + a))
                screen_buttons['event'].check()
                a += 150"""

        # buttons
        buttons.draw_button((50, 50), text='< Back to Main Menu', cur_screen='start screen')
        buttons.draw_button((330, 70), text='EVENTS', available=False)
        buttons.draw_button((410, 70), text='CLAN', cur_screen='clan screen')


class ProfileScreen(Screens):
    def on_use(self):
        # LAYOUT
        verdana.text('PROFILE', ('center', 70))
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

        # buttons
        buttons.draw_button(('center', -150), text='Back', cur_screen='clan screen')


class SingleEventScreen(Screens):
    def on_use(self):
        # LAYOUT
        if game.switches['event'] is not None:
            events_class.all_events[game.switches['event']].page()

        # buttons
        buttons.draw_button(('center', -150), text='Continue', cur_screen='events screen')

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
