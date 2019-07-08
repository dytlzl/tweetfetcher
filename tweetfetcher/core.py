import requests
from bs4 import BeautifulSoup
from .tweet import Tweet
import urllib.parse
import random
import time


class GenericFetcher:
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_%s) " \
                 "Chrome/42.0.%s.%s Safari/%s.%s WebBrowser/36.%s"
    json_url = None
    tweets = None
    params = None
    filename = None
    max_count = None
    random.seed()

    def fetch(self):
        self.fetch_tweets()
        for tweet in self.tweets:
            tweet.shape_text()
            tweet.pop_media()

    def fetch_tweets(self):
        params = urllib.parse.urlencode(self.params, quote_via=urllib.parse.quote)
        headers = {
            "User-Agent": self.USER_AGENT % (
                random.randrange(1, 7),
                random.randrange(100),
                random.randrange(100),
                random.randrange(521, 538),
                random.randrange(1, 37),
                random.randrange(100))
        }
        res = requests.get(self.json_url, params=params, headers=headers)
        res_json = res.json()
        soup = BeautifulSoup(res_json['items_html'], 'html.parser')
        items = soup.select('.js-stream-item')
        for item in items:
            try:
                self.tweets.append(
                    Tweet(
                        item.get('data-item-id'),
                        item.select_one('.fullname').get_text(),
                        item.select_one('.username').get_text(),
                        item.select_one('.tweet-timestamp')['title'],
                        int(item.select_one('._timestamp')['data-time']),
                        item.select_one('.js-tweet-text-container').get_text(),
                        [
                            int(item.select('.ProfileTweet-actionCount')[0]['data-tweet-stat-count']),
                            int(item.select('.ProfileTweet-actionCount')[1]['data-tweet-stat-count']),
                            int(item.select('.ProfileTweet-actionCount')[2]['data-tweet-stat-count'])
                        ],
                    )
                )
            except AttributeError:
                print('AttributeError\n')
                continue
            print('\rFetched %s Tweets %s' % (len(self.tweets), self.tweets[-1].datetime), end='')
            if len(self.tweets) >= self.max_count:
                print(' Done')
                return
        if 'min_position' in res_json:
            time.sleep(random.uniform(0.2, 0.8))
            if self.params['max_position'] == res_json['min_position']:
                return
            self.params['max_position'] = res_json['min_position']
            self.fetch_tweets()

    def write_text(self):
        with open(self.filename, mode='w', encoding='utf-8') as file:
            file.write('tweets_count: %s\n\n' % len(self.tweets))
            count = 0
            for item in self.tweets:
                count += 1
                text = 'index: %s,\n' % count \
                       + 'tweet_id: %s,\n' % item.id \
                       + 'username: %s(%s),\n' % (item.screen_name, item.username) \
                       + 'time: %s(%s),\n' % (item.datetime, item.timestamp) \
                       + 'media_id: %s,\n' % item.media_id \
                       + 'tweet_text: {\n%s\n}\n' % item.text \
                       + 'reply/retweet/like: %s/%s/%s\n' \
                       % (item.reply_count(), item.retweet_count(), item.like_count()) \
                       + '\n'
                file.write(text)
