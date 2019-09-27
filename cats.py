from pelts import *
from names import *
from sprites import *
from game_essentials import *
from random import choice, randint


class Cat(object):
    used_screen = screen
    traits = ['ambitious', 'loyal', 'righteous', 'fierce', 'nervous', 'strict', 'charismatic', 'calm',
              'daring', 'loving', 'playful', 'bitter', 'lonesome', 'troublesome', 'insecure', 'vengeful',
              'shameless']
    kit_traits = ['bouncy', 'bullying', 'daydreamer', 'nervous', 'charming', 'attention-seeker',
                  'inquisitive', 'bossy', 'troublesome', 'quiet', 'daring', 'sweet', 'insecure']
    ages = ['kitten', 'adolescent', 'young adult', 'adult', 'adult', 'senior adult', 'elder']
    gender_tags = {'female': 'F', 'male': 'M'}
    skills = ['good hunter', 'great hunter', 'fantastic hunter', 'smart', 'very smart', 'extremely smart',
              'good fighter', 'great fighter', 'excellent fighter', 'good speaker', 'great speaker',
              'excellent speaker', 'strong connection to starclan', 'good teacher', 'great teacher',
              'fantastic teacher']

    all_cats = {}

    def __init__(self, prefix=None, gender=None, status="kitten", parent1=None, parent2=None, pelt=None,
                 eye_colour=None, suffix=None, ID=None):
        self.gender = gender
        self.status = status
        self.age = None
        self.parent1 = parent1
        self.parent2 = parent2  # if parent1 is None, parent2 is too
        self.pelt = pelt
        self.eye_colour = eye_colour
        self.mentor = None
        self.placement = None

        # ID
        if ID is None:
            self.ID = str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(
                randint(0, 9))
        else:
            self.ID = ID

        # personality trait and skill
        if self.status != 'kitten':
            # TRAIT
            a = randint(0, 50)
            if a == 1:
                self.trait = 'strange'
            elif a == 2:
                self.trait = 'bloodthirsty'
            else:
                self.trait = choice(self.traits)

            # SKILL
            if self.status != 'apprentice':
                self.skill = choice(self.skills)
            else:
                self.skill = '???'
        else:
            self.trait = self.trait = choice(self.kit_traits)
            self.skill = '???'

        # gender
        if self.gender is None:
            self.gender = choice(["female", "male"])
        self.g_tag = self.gender_tags[self.gender]

        # age
        if status is None:
            self.age = choice(self.ages)
        else:
            if status in ['kitten', 'elder']:
                self.age = status
            elif status == 'apprentice':
                self.age = 'adolescent'
            else:
                self.age = choice(['young adult', 'adult', 'adult', 'senior adult'])

        # eye colour
        if self.eye_colour is None:
            a = randint(0, 200)
            if a == 1:
                self.eye_colour = choice(["BLUEYELLOW", "BLUEGREEN"])
            else:
                if self.parent1 is None:
                    self.eye_colour = choice(eye_colours)
                elif self.parent2 is None:
                    self.eye_colour = choice([self.parent1.eye_colour, choice(eye_colours)])
                else:
                    self.eye_colour = choice([self.parent1.eye_colour, self.parent2.eye_colour, choice(eye_colours)])

        # pelt
        if self.pelt is None:
            if self.parent1 is None:
                # If pelt has not been picked manually, this function chooses one based on possible inheritances
                self.pelt = choose_pelt(self.gender)

            elif self.parent2 is None and self.parent1 in self.all_cats.keys():
                # 1 in 3 chance to inherit a single paren't pelt
                par1 = self.all_cats[self.parent1]
                self.pelt = choose_pelt(self.gender, choice([par1.pelt.colour, None]),
                                        choice([par1.pelt.white, None]),
                                        choice([par1.pelt.name, None]),
                                        choice([par1.pelt.length, None]))

            elif self.parent1 in self.all_cats.keys() and self.parent2 in self.all_cats.keys():
                # 2 in 3 chance to inherit either parent's pelt
                par1 = self.all_cats[self.parent1]
                par2 = self.all_cats[self.parent2]
                self.pelt = choose_pelt(self.gender, choice([par1.pelt.colour, par2.pelt.colour, None]),
                                        choice([par1.pelt.white, par2.pelt.white, None]),
                                        choice([par1.pelt.name, par2.pelt.name, None]),
                                        choice([par1.pelt.length, par2.pelt.length, None]))

        # NAME
        if self.pelt is not None:
            self.name = Name(status, prefix, suffix, self.pelt.colour, self.eye_colour, self.pelt.name)
        else:
            self.name = Name(status, prefix, suffix, eyes=self.eye_colour)

        # SPRITE
        self.status_sprites = {'kitten': randint(0, 2), 'apprentice': randint(3, 5), 'elder': randint(3, 5)}
        self.reverse = choice([True, False])
        self.skin = choice(skin_sprites)

        # scars & more
        if self.age in ['kitten', 'adolescent']:
            i = randint(0, 15)
        elif self.age in ['young adult', 'adult']:
            i = randint(0, 7)
        else:
            i = randint(0, 3)
        if i == 1:
            self.specialty = choice([choice(scars1), choice(scars2)])
        else:
            self.specialty = None
        # -

        if self.pelt is not None:
            if self.pelt.length != 'long':
                self.status_sprites['warrior'] = randint(6, 8)
            else:
                self.status_sprites['warrior'] = randint(0, 2)
            if self.age != 'elder':
                self.status_sprites['medicine cat'] = self.status_sprites['warrior']
                self.status_sprites['leader'] = self.status_sprites['warrior']
            else:
                self.status_sprites['medicine cat'] = self.status_sprites['elder']
                self.status_sprites['leader'] = self.status_sprites['elder']

            # WHITE PATCHES
            if self.pelt.white and self.pelt.white_patches is not None:
                a = randint(0, 10)
                if a == 1 and self.pelt.name in ['Calico', 'TwoColour', 'Tabby', 'Speckled']\
                        and self.pelt.colour != 'WHITE':
                    self.white_patches = choice(['COLOURPOINT', 'COLOURPOINTCREAMY'])
                elif a == 1 and self.pelt.name in ['Calico', 'TwoColour', 'Tabby', 'Speckled']:
                    self.white_patches = 'COLOURPOINT'
                elif self.pelt.name in ['Tabby', 'Speckled', 'TwoColour'] and self.pelt.colour == 'WHITE':
                    self.white_patches = choice(['ANY', 'TUXEDO', 'LITTLE', 'VAN'])
                else:
                    self.white_patches = choice(self.pelt.white_patches)
            else:
                self.white_patches = None

            # pattern for tortie/calico cats
            if self.pelt.name == 'Calico':
                self.pattern = choice(calico_pattern)
            elif self.pelt.name == 'Tortie':
                self.pattern = choice(tortie_pattern)
            else:
                self.pattern = None
        else:
            self.white_patches = None
            self.pattern = None

        # Sprite sizes
        self.sprite = None
        self.big_sprite = None
        self.large_sprite = None

        # SAVE CAT INTO ALL_CATS DICTIONARY IN CATS -CLASS
        self.all_cats[self.ID] = self

    def __repr__(self):
        return self.ID

    def status_change(self, new_status):
        # revealing of traits and skills
        if self.status == 'kitten':
            a = randint(0, 50)
            if a == 1:
                self.trait = 'strange'
            else:
                self.trait = choice(self.traits)
        if self.status == 'apprentice':
            self.skill = choice(self.skills)

        # getting new scars with age
        if self.specialty is False:
            if self.age in ['kitten', 'adolescent']:
                i = randint(0, 15)
            elif self.age in ['young adult', 'adult']:
                i = randint(0, 7)
            else:
                i = randint(0, 3)
            if i == 1:
                self.specialty = choice([choice(scars1), choice(scars2)])
            else:
                self.specialty = None

        self.status = new_status
        self.name.status = new_status

        # update class dictionary
        self.all_cats[self.ID] = self

    def update_sprite(self):
        # First make pelt, if it wasn't possible before

        if self.pelt is None:
            if self.parent1 is None:
                # If pelt has not been picked manually, this function chooses one based on possible inheritances
                self.pelt = choose_pelt(self.gender)

            elif self.parent2 is None and self.parent1 in self.all_cats.keys():
                # 1 in 3 chance to inherit a single paren't pelt
                par1 = self.all_cats[self.parent1]
                self.pelt = choose_pelt(self.gender, choice([par1.pelt.colour, None]),
                                        choice([par1.pelt.white, None]),
                                        choice([par1.pelt.name, None]),
                                        choice([par1.pelt.length, None]))

            elif self.parent1 in self.all_cats.keys() and self.parent2 in self.all_cats.keys():
                # 2 in 3 chance to inherit either parent's pelt
                par1 = self.all_cats[self.parent1]
                par2 = self.all_cats[self.parent2]
                self.pelt = choose_pelt(self.gender, choice([par1.pelt.colour, par2.pelt.colour, None]),
                                        choice([par1.pelt.white, par2.pelt.white, None]),
                                        choice([par1.pelt.name, par2.pelt.name, None]),
                                        choice([par1.pelt.length, par2.pelt.length, None]))
            else:
                self.pelt = choose_pelt(self.gender)

        if self.status_sprites['warrior'] is None:
            if self.pelt.length != 'long':
                self.status_sprites['warrior'] = randint(6, 8)
            else:
                self.status_sprites['warrior'] = randint(0, 2)
        if self.age != 'elder':
            self.status_sprites['medicine cat'] = self.status_sprites['warrior']
            self.status_sprites['leader'] = self.status_sprites['warrior']
        else:
            self.status_sprites['medicine cat'] = self.status_sprites['elder']
            self.status_sprites['leader'] = self.status_sprites['elder']

        # THE SPRITE UPDATE
        # draw colour & style
        new_sprite = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)

        if self.pelt.name not in ['Tortie', 'Calico']:
            if self.pelt.length == 'long' and self.status not in ['kitten', 'apprentice'] or self.age == 'elder':
                new_sprite.blit(
                    sprites.sprites[self.pelt.sprites[1] + 'extra' + self.pelt.colour + str(
                        self.status_sprites[self.status])], (0, 0))
            else:
                new_sprite.blit(
                    sprites.sprites[self.pelt.sprites[1] + self.pelt.colour + str(self.status_sprites[self.status])],
                    (0, 0))
        else:
            if self.pelt.length == 'long' and self.status not in ['kitten', 'apprentice'] or self.age == 'elder':
                new_sprite.blit(
                    sprites.sprites[self.pelt.sprites[1] + 'extra' + self.pattern + str(
                        self.status_sprites[self.status])], (0, 0))
            else:
                new_sprite.blit(
                    sprites.sprites[self.pelt.sprites[1] + self.pattern + str(self.status_sprites[self.status])],
                    (0, 0))

        # draw white patches
        if self.white_patches is not None:
            if self.pelt.length == 'long' and self.status not in ['kitten', 'apprentice'] or self.age == 'elder':
                new_sprite.blit(
                    sprites.sprites['whiteextra' + self.white_patches + str(self.status_sprites[self.status])],
                    (0, 0))
            else:
                new_sprite.blit(
                    sprites.sprites['white' + self.white_patches + str(self.status_sprites[self.status])], (0, 0))

        # draw eyes & scars1
        if self.pelt.length == 'long' and self.status not in ['kitten', 'apprentice'] or self.age == 'elder':
            if self.specialty in scars1:
                new_sprite.blit(sprites.sprites['scarsextra' + self.specialty + str(self.status_sprites[self.status])],
                                (0, 0))
            new_sprite.blit(sprites.sprites['eyesextra' + self.eye_colour + str(self.status_sprites[self.status])],
                            (0, 0))
        else:
            if self.specialty in scars1:
                new_sprite.blit(sprites.sprites['scars' + self.specialty + str(self.status_sprites[self.status])],
                                (0, 0))
            new_sprite.blit(sprites.sprites['eyes' + self.eye_colour + str(self.status_sprites[self.status])], (0, 0))

        # draw line art
        if self.pelt.length == 'long' and self.status not in ['kitten', 'apprentice'] or self.age == 'elder':
            new_sprite.blit(sprites.sprites['lines' + str(self.status_sprites[self.status] + 9)], (0, 0))
        else:
            new_sprite.blit(sprites.sprites['lines' + str(self.status_sprites[self.status])], (0, 0))

        # draw skin and scars2
        if self.pelt.length == 'long' and self.status not in ['kitten', 'apprentice'] or self.age == 'elder':
            new_sprite.blit(sprites.sprites['skinextra' + self.skin + str(self.status_sprites[self.status])], (0, 0))
            if self.specialty in scars2:
                new_sprite.blit(sprites.sprites['scarsextra' + self.specialty + str(self.status_sprites[self.status])],
                                (0, 0))
        else:
            new_sprite.blit(sprites.sprites['skin' + self.skin + str(self.status_sprites[self.status])], (0, 0))
            if self.specialty in scars2:
                new_sprite.blit(sprites.sprites['scars' + self.specialty + str(self.status_sprites[self.status])],
                                (0, 0))

        # reverse, if assigned so
        if self.reverse:
            new_sprite = pygame.transform.flip(new_sprite, True, False)

        # apply
        self.sprite = new_sprite
        self.big_sprite = pygame.transform.scale(new_sprite, (sprites.new_size, sprites.new_size))
        self.large_sprite = pygame.transform.scale(self.big_sprite, (sprites.size*3, sprites.size*3))

        # update class dictionary
        self.all_cats[self.ID] = self

    def draw(self, pos):
        new_pos = list(pos)
        if pos[0] == 'center':
            new_pos[0] = screen_x/2 - sprites.size/2
        elif pos[0] < 0:
            new_pos[0] = screen_x + pos[0] - sprites.size
        self.used_screen.blit(self.sprite, new_pos)

    def draw_big(self, pos):
        new_pos = list(pos)
        if pos[0] == 'center':
            new_pos[0] = screen_x / 2 - sprites.new_size / 2
        elif pos[0] < 0:
            new_pos[0] = screen_x + pos[0] - sprites.new_size
        self.used_screen.blit(self.big_sprite, new_pos)

    def draw_large(self, pos):
        new_pos = list(pos)
        if pos[0] == 'center':
            new_pos[0] = screen_x / 2 - sprites.size*3 / 2
        elif pos[0] < 0:
            new_pos[0] = screen_x + pos[0] - sprites.size*3
        self.used_screen.blit(self.large_sprite, new_pos)

    def save_cats(self):
        data = ''
        for x in self.all_cats.values():
            # cat ID -- name prefix : name suffix
            data += x.ID + '\t' + x.name.prefix + ':' + x.name.suffix + '\t'
            # cat gender -- status -- age -- trait
            data += x.gender + '\t' + x.status + '\t' + str(x.age) + '\t' + x.trait + '\t'
            # cat parent1 -- parent2 -- mentor
            if x.parent1 is None:
                data += 'None \t'
            else:
                data += x.parent1.ID + '\t'
            if x.parent2 is None:
                data += 'None \t'
            else:
                data += x.parent2.ID + '\t'
            if x.mentor is None:
                data += 'None \t'
            else:
                data += x.mentor.ID + '\t'

            # pelt type -- colour -- white -- length
            data += x.pelt.name + '\t' + x.pelt.colour + '\t' + str(x.pelt.white) + '\t' + x.pelt.length + '\t'
            # sprite kitten -- apprentice
            data += str(x.status_sprites['kitten']) + '\t' + str(x.status_sprites['apprentice']) + '\t'
            # sprite warrior -- elder
            data += str(x.status_sprites['warrior']) + '\t' + str(x.status_sprites['elder']) + '\t'
            # eye colour -- reverse -- white patches -- pattern
            data += x.eye_colour + '\t' + str(x.reverse) + '\t' + str(x.white_patches) + '\t' + str(x.pattern) + '\t'
            # skin -- skill -- NONE  -- specs
            data += x.skin + '\t' + x.skill + '\t' + 'None' + '\t' + str(x.specialty)

            # next cat
            data += '\n'

        # remove one last unnecessary new line
        data = data[:-1]

        with open('saves/cats.txt', 'w') as write_file:
            write_file.write(data)

    def load_cats(self):
        with open('saves/cats.txt', 'r') as read_file:
            cat_data = read_file.read()

        if len(cat_data) > 0:
            for i in cat_data.split('\n'):
                # CAT: ID(0) - prefix:suffix(1) - gender(2) - status(3) - age(4) - trait(5) - parent1(6) - parent2(7)
                #  - mentor(8)
                # PELT: pelt(9) - colour(10) - white(11) - length(12)
                # SPRITE: kitten(13) - apprentice(14) - warrior(15) - elder(16) - eye colour(17) - reverse(18)
                # - white patches(19) - pattern(20) - skin(21) - skill(22) - NONE(23) - spec(24)

                attr = i.split('\t')
                for x in range(len(attr)):
                    if attr[x] in ['None', 'None ']:
                        attr[x] = None
                    elif attr[x] == 'True':
                        attr[x] = True
                    elif attr[x] == 'False':
                        attr[x] = False

                the_pelt = choose_pelt(attr[2], attr[10], attr[11], attr[9], attr[12], True)
                the_cat = Cat(ID=attr[0], prefix=attr[1].split(':')[0], suffix=attr[1].split(':')[1], gender=attr[2],
                              status=attr[3], pelt=the_pelt, parent1=attr[6], parent2=attr[7], eye_colour=attr[17])
                the_cat.age, the_cat.mentor = attr[4], attr[8]
                the_cat.status_sprites['kitten'], the_cat.status_sprites['apprentice'] = int(attr[13]), int(attr[14])
                the_cat.status_sprites['warrior'], the_cat.status_sprites['elder'] = int(attr[15]), int(attr[16])
                the_cat.status_sprites['medicine cat'], the_cat.status_sprites['leader'] = int(attr[15]), int(attr[15])
                the_cat.reverse, the_cat.white_patches, the_cat.pattern = attr[18], attr[19], attr[20]
                the_cat.trait, the_cat.skin, the_cat.specialty = attr[5], attr[21], attr[24]
                if isinstance(attr[24], str):
                    the_cat.skill = attr[22]
                else:
                    the_cat.skill = attr[22]
                self.all_cats[the_cat.ID] = the_cat

            for n in self.all_cats.values():
                n.update_sprite()


# CAT CLASS ITEMS
cat_class = Cat()

# The randomized cat sprite in Main Menu screen
example_cat = Cat(status=choice(["kitten", "apprentice", "warrior", "elder"]))
example_cat.update_sprite()


# Twelve example cats
def example_cats():
    e = random.sample(range(12), 2)
    for a in range(12):
        if a in e:
            game.choose_cats[a] = Cat(status='warrior')
        else:
            game.choose_cats[a] = Cat(status=choice(['kitten', 'apprentice', 'warrior', 'warrior', 'elder']))
        game.choose_cats[a].update_sprite()
