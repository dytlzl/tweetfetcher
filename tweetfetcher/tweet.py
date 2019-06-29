from datetime import datetime


class Tweet:
    URL = 'https://twitter.com/%s/status/%s'

    def __init__(self, *args):
        self.id = args[0]
        self.screen_name = args[1]
        self.username = args[2]
        self.datetime_origin = args[3]
        self.timestamp = args[4]
        self.text = args[5]
        self.counts = args[6]
        self.media_id = None
        self.reply_count = lambda: self.counts[0]
        self.retweet_count = lambda: self.counts[1]
        self.like_count = lambda: self.counts[2]
        self.datetime = datetime.fromtimestamp(self.timestamp)
        self.url = self.URL % (
            self.username,
            self.id
        )

    def pop_media(self):
        if 'pic.twitter.com/' in self.text:
            text_split = self.text.split('pic.twitter.com/')
            self.text = text_split[0]
            self.media_id = text_split[1]

    def shape_text(self):
        self.text = self.text.replace('\xa0', u' ')
        if self.text[0:1] == '\n':
            self.text = self.text[1:-1]

    def generate_list(self):
        return [self.id,
                self.screen_name,
                self.username,
                self.datetime,
                self.timestamp,
                self.media_id,
                *self.counts,
                self.text]
