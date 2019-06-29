from .core import GenericFetcher


class Search(GenericFetcher):
    TWITTER_URL = 'https://twitter.com/i/search/timeline'

    def __init__(self, search_word, max_count=20, since=None, until=None, lang=None):
        self.tweets = []
        self.max_count = max_count
        if since is not None:
            search_word += ' since:' + since
        if until is not None:
            search_word += ' until:' + until
        print(search_word)
        self.params = {
            'f': 'tweets',
            'vertical': 'default',
            'q': search_word,
            'include_available_features': 1,
            'include_entities': 1,
            'max_position': '',
            'reset_error_state': 'false',
        }
        if lang is not None:
            self.params['l'] = lang
        self.filename = 'tweets_search_' + search_word + '.txt'
        self.json_url = self.TWITTER_URL
