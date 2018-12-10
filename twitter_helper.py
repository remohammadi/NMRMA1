# coding: utf-8

from datetime import datetime
import json
from os.path import abspath, dirname, exists, join, realpath

from twitter import Status, User


HERE = abspath(dirname(realpath(__file__)))
FLAGS = {
    'AF': '🇦🇫',
    'AR': '🇦🇷',
    'AU': '🇦🇺',
    'BR': '🇧🇷',
    'CA': '🇨🇦',
    'CN': '🇨🇳',
    'DE': '🇩🇪',
    'EU': '🇪🇺',
    'FR': '🇫🇷',
    'IN': '🇮🇳',
    'ID': '🇮🇩',
    'IR': '🇮🇷',
    'IL': '🇮🇱',
    'IT': '🇮🇹',
    'JP': '🇯🇵',
    'KR': '🇰🇷',
    'MX': '🇲🇽',
    'NL': '🇳🇱',
    'PK': '🇵🇰',
    'RU': '🇷🇺',
    'SA': '🇸🇦',
    'TR': '🇹🇷',
    'UK': '🇬🇧',
    'UN': '🇺🇳',
    'US': '🇺🇸',
    'ZA': '🇿🇦',
}


class Account(object):
    def __init__(self, name, twitter_handler, country_representing, role, is_personal, verified):
        self.name = name
        self.twitter_handler = twitter_handler
        self.country_representing = country_representing
        self.role = role
        self.is_personal = is_personal
        self.verified = verified
        self.followings = []
        self.tweets = []
        self.fetch_timestamp = None
        self.filename = join(HERE, 'data', 'account-%s.json' % self.twitter_handler)

    def save(self):
        data = {
            'followings': [f._json for f in self.followings],
            'tweets': [t._json for t in self.tweets],
            'fetch_timestamp': self.fetch_timestamp,
        }
        with open(self.filename, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=1, separators=(',', ': '))

    def load(self):
        if not exists(self.filename):
            return False
        with open(self.filename, 'r') as infile:
            data = json.load(infile)
            self.followings = [User.NewFromJsonDict(f) for f in data['followings']]
            self.tweets = [Status.NewFromJsonDict(t) for t in data['tweets']]
            self.fetch_timestamp = data['fetch_timestamp']
            return self.fetch_timestamp is not None

    def fetch(self, api, from_internet_even_if_local_exists=False, save=True):
        if from_internet_even_if_local_exists or not self.load():
            self.followings = api.GetFriends(screen_name=self.twitter_handler)
            self.tweets = api.GetUserTimeline(screen_name=self.twitter_handler, count=200)
            self.fetch_timestamp = str(datetime.now())
            if save:
                self.save()
            return True
        return False

    def __str__(self):
        text = self.name or self.twitter_handler
        if self.country_representing in FLAGS:
            text += ' ' + FLAGS[self.country_representing]
        return text

    def verbose_title(self):
        text = self.name or self.twitter_handler
        if self.verified:
            text += '✅'
        if self.country_representing in FLAGS:
            text += " ("
            if self.role:
                text += self.role + " of "
            text += self.country_representing + ' ' + FLAGS[self.country_representing] + ")"
        return text
