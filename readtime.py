import re
import math

from pelican import signals
from HTMLParser import HTMLParser


# http://en.wikipedia.org/wiki/Words_per_minute
WPM = 200.0


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def calculate_readtime(content_object):
    if content_object._content is not None:
        content = content_object._content

        text = strip_tags(content)
        words = re.split(r'[^0-9A-Za-z]+', text)

        num_words = len(words)
        minutes = int(math.ceil(num_words / WPM))
        if minutes == 0:
            minutes = 1

        content_object.readtime = {
            "minutes": minutes,
        }


def register():
    signals.content_object_init.connect(calculate_readtime)

