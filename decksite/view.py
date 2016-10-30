import html
import re

from flask import url_for

from magic import mana
from shared import dtutil

from decksite import deck_name
from decksite import template

NAME_MAX_LEN = 35

# pylint: disable=no-self-use
class View:
    def template(self):
        return self.__class__.__name__.lower()

    def content(self):
        return template.render(self)

    def page(self):
        return template.render_name('page', self)

    def home_url(self):
        return url_for('home')

    def css_url(self):
        return url_for('static', filename='css/pd.css')

    def menu(self):
        return [
            {'name': 'Home', 'url': url_for('home')},
            {'name': 'People', 'url': url_for('people')},
            {'name': 'Cards', 'url': url_for('cards')}
        ]

    def favicon_url(self):
        return url_for('favicon', rest='.ico')

    def favicon_152_url(self):
        return url_for('favicon', rest='-152.png')

    def title(self):
        if not self.subtitle():
            return 'Penny Dreadful Decks'
        else:
            return '{subtitle} – Penny Dreadful Decks'.format(subtitle=self.subtitle())

    def subtitle(self):
        return None

    def prepare(self):
        self.prepare_decks()
        self.prepare_cards()

    def prepare_decks(self):
        for d in getattr(self, 'decks', []):
            if d.finish == 1:
                d.top8 = '①'
                d.stars = '★★★'
            elif d.finish == 2:
                d.top8 = '②'
                d.stars = '★★'
            elif d.finish == 3:
                d.top8 = '④'
                d.stars = '★★'
            elif d.finish == 5:
                d.top8 = '⑧'
                d.stars = '★'
            else:
                d.top8 = ''
                if d.wins - 5 >= d.losses:
                    d.stars = '★★'
                elif d.wins - 3 >= d.losses:
                    d.stars = '★'
                else:
                    d.stars = ''
            d.colors_safe = colors_html(d.colors)
            name = deck_name.normalize(d)
            d.name = name[0:NAME_MAX_LEN - 1] + '…' if len(name) > NAME_MAX_LEN else name
            d.person_url = url_for('person', person_id=d.person_id)
            d.date = dtutil.display_date(d.date)

    def prepare_cards(self):
        for c in getattr(self, 'cards', []):
            c.url = url_for('card', name=c.name)

def colors_html(colors):
    s = ''.join(mana.order(colors))
    n = len(colors)
    return re.sub('([WUBRG])', r'<span class="mana mana-{n} mana-\1"></span>'.format(n=n), html.escape(s))