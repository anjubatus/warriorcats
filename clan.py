from cats import *
from text import *


class Clan(object):
    leader_lives = 9
    clan_cats = []
    warriors = {}
    apprentices = {}
    kittens = {}
    elders = {}

    layout_1 = {'leader den': ('center', 100), 'medicine den': (100, 230), 'nursery': (-100, 230),
                'clearing': ('center', 300), 'apprentice den': (100, 450), 'warrior den': (-100, 450),
                'elder den': ('center', 500),
                'leader place': [('center', 120), (screen_x/2-50, 170), (screen_x/2, 170)],
                'medicine place': [(70, 250), (120, 250), (170, 250), (100, 300), (150, 300)],
                'nursery place': [(-100, 250), (-150, 250), (-200, 250), (-70, 300), (-120, 300), (-170, 300),
                                  (-220, 300), (-70, 350), (-120, 350), (-170, 350), (-220, 350)],
                'clearing place': [('center', 320), (300, 370), (350, 370), (400, 370), (300, 420), (350, 420),
                                   (400, 420)],
                'apprentice place': [(70, 470), (120, 470), (170, 470), (100, 520), (150, 520), (200, 520)],
                'warrior place': [(-50, 470), (-100, 490), (-150, 470), (-200, 490), (-50, 520), (-100, 540),
                                  (-150, 520), (-200, 540)],
                'elder place': [(300, 520), (350, 520), (400, 520), (320, 570), (370, 570)]}

    cur_layout = layout_1
    places_vacant = {'leader': [False, False, False], 'medicine': [False, False, False, False, False],
                     'nursery': [False, False, False, False, False, False, False, False, False, False, False],
                     'clearing': [False, False, False, False, False, False, False],
                     'apprentice': [False, False, False, False, False, False],
                     'warrior': [False, False, False, False, False, False, False, False],
                     'elder': [False, False, False, False, False]}

    def __init__(self, name=None, leader=None, medicine_cat=None):
        if name is not None:
            self.name = name

            self.leader = leader
            self.leader.status_change('leader')
            self.leader_predecessors = 0
            self.clan_cats.append(self.leader.ID)

            self.medicine_cat = medicine_cat
            self.medicine_cat.status_change('medicine cat')
            self.med_cat_predecessors = 0
            self.clan_cats.append(self.medicine_cat.ID)

            self.age = 0
        else:
            self.name = None

    def add_cat(self, cat):  # cat is a 'Cat' object
        if cat.ID in cat_class.all_cats.keys() and cat.ID not in self.clan_cats:
            self.clan_cats.append(cat.ID)
            if cat.status == 'kitten':
                self.kittens[str(cat.ID)] = cat
            elif cat.status == 'apprentice':
                self.apprentices[str(cat.ID)] = cat
            elif cat.status == 'warrior':
                self.warriors[str(cat.ID)] = cat
            elif cat.status == 'elder':
                self.elders[str(cat.ID)] = cat

    def remove_cat(self, ID):  # ID is cat.ID
        if ID in cat_class.all_cats.keys():
            cat_class.all_cats.pop(ID)
            if ID in self.clan_cats:
                self.clan_cats.remove(ID)

    def __repr__(self):
        if self.name is not None:
            return self.name + ': led by ' + str(self.leader.name) + ' with ' + str(
                self.medicine_cat.name) + ' as med. cat'
        else:
            return 'No clan'

    def save_clan(self):
        # clan name - clan age
        data = self.name + '\t' + str(self.age) + '\n'

        # leader ID - leader lives - number of leader predecessors
        data = data + self.leader.ID + '\t' + str(self.leader_lives) + '\t' + str(self.leader_predecessors) + '\n'

        # med. cat ID - number of med. cat predecessors
        data = data + self.medicine_cat.ID + '\t' + str(self.med_cat_predecessors) + '\n'

        # other members
        for a in range(len(self.clan_cats)):
            if a != len(self.clan_cats) - 1:
                if self.clan_cats[a] in cat_class.all_cats.keys():
                    data = data + self.clan_cats[a] + '\t'
            else:
                data = data + self.clan_cats[a]

        # save data
        with open('saves/clan.txt', 'w') as write_file:
            write_file.write(data)

    def load_clan(self):
        with open('saves/clan.txt', 'r') as read_file:
            clan_data = read_file.read()

        sections = clan_data.split('\n')

        general = sections[0].split('\t')  # clan name(0) - clan age(1)
        leader_info = sections[1].split('\t')  # leader ID(0) - leader lives(1) - leader predecessors(2)
        med_cat_info = sections[2].split('\t')  # med cat ID(0) - med cat predecessors(2)
        members = sections[3].split('\t')  # rest of the members in order

        game.clan = Clan(general[0], cat_class.all_cats[leader_info[0]], cat_class.all_cats[med_cat_info[0]])
        game.clan.age = int(general[1])
        game.clan.leader_lives, game.clan.leader_predecessors = int(leader_info[1]), int(leader_info[2])
        game.clan.med_cat_predecessors = int(med_cat_info[1])

        for x in members:
            if x in cat_class.all_cats.keys():
                game.clan.add_cat(cat_class.all_cats[x])
            else:
                print 'cat not found:', x


clan_class = Clan()

# remove non-existent cats
clan_class.remove_cat(cat_class.ID)
clan_class.remove_cat(example_cat.ID)

