import re

from pelican import signals
from HTMLParser import HTMLParser


# http://en.wikipedia.org/wiki/Words_per_minute
WPM = 200


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


def calculate_readtime(instance):
    if instance._content is not None:
        content = instance._content

        text = strip_tags(content)
        words = re.split(r'[^0-9A-Za-z]+', text)

        minutes = len(words) / WPM
        if minutes == 0:
            minutes = 1

        instance.readtime = {
            "minutes": minutes,
        }


def register():
    signals.content_object_init.connect(calculate_readtime)

