from buttons import *
from cats import *


class Events(object):
    all_events = {}

    def __init__(self, name=None):
        self.name = name
        if name is not None:
            self.all_events[name] = self
        self.par1 = None
        self.par2 = None

    def day(self):
        if len(self.all_events) > 0:
            for i in self.all_events.values():
                e = randint(0, 3)
                if e == 1:
                    # print "event added..."
                    game.cur_events[i.name] = i

    def news(self, pos):  # the layout for short squabble on the 'events' page, where you can click for the real page
        pass

    def page(self):  # the events bigger and more detailed page were you can take action
        pass


# events child classes
class IllnessEvent(Events):
    def init(self, par1=None):
        if par1 is None:
            self.par1 = 'greencough'  # default illness is greencough
        else:
            self.par1 = par1

    def news(self, pos):
        header = self.par1[0].upper() + self.par1[1:] + ' outbreak!'
        verdana_big.text(header, pos)
        verdana.text('Cats have been infected! Action needs to be taken quickly before it spreads.',
                     (pos[0], pos[1] + 25))
        buttons.draw_button(('center', pos[1]+50), text='Complete', cur_screen='event screen', event='illness')

    def page(self):
        header = self.par1[0].upper() + self.par1[1:] + ' outbreak!'
        verdana_big.text(header, ('center', 100))


class CeremonyEvent(Events):
    def init(self, par1, par2=None):
        # par2 is what kind of ceremony ex. leader cer., par1 is the ID of cat in question
        if par2 is None:
            self.par2 = 'Leader'
        else:
            self.par2 = par2
        if par1 is None:
            print 'Cat not selected for ceremony!'
        else:
            self.par1 = par1

    def news(self, pos):
        header = self.par2 + ' ceremony is about to be held!'
        verdana_big.text(header, pos)
        verdana.text('Come join the cats at the clearing.',
                     (pos[0], pos[1] + 25))
        buttons.draw_button(('center', pos[1] + 50), text='Complete', cur_screen='event screen', event='ceremony')

    def page(self):
        header = self.par1[0].upper() + self.par1[1:] + ' ceremony!'
        verdana_big.text(header, ('center', 100))


events_class = Events()

# EVENT DETAILS & INIT.
greencough = IllnessEvent('Greencough Outbreak')
leader_cer = CeremonyEvent('Leader Ceremony')
