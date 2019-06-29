from .core import GenericFetcher


class User(GenericFetcher):
    TWITTER_URL = 'https://twitter.com/i/profiles/show/%s/timeline/tweets'

    def __init__(self, username, max_count=20):
        self.position = ''
        self.tweets = []
        self.max_count = max_count
        self.params = {
            'include_available_features': 1,
            'include_entities': 1,
            'max_position': '',
            'reset_error_state': 'false',
        }
        self.json_url = self.TWITTER_URL % username
        self.filename = 'tweets_user_' + username + '.txt'
