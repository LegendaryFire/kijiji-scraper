import os
from constants import API_SEARCH_ENDPOINT
from urllib import parse
import yaml


class SearchQuery:
    def __init__(self, data):
        self.__data = data

    def get_search(self) -> str:
        """
        The name of the search.
        :return: Returns the name of the search.
        """
        return self.__data.get('search')

    def include_business(self) -> bool:
        """
        Whether to include business ads or not.
        :return: True if including business ads.
        """
        value = self.__data.get('include_business')
        return value if value is not None else False

    def send_notifications(self) -> bool:
        """
        Whether to send notifications or not.
        :return: True if sending notifications.
        """
        value = self.__data.get('send_notification')
        return value if value is not None else False

    def build_url(self) -> str:
        """
        Builds the search URL for the given search query.
        :return: Returns the generated search URL.
        """
        url_parameters = parse.urlencode(self.__data.get('params'))
        return f'{API_SEARCH_ENDPOINT}{url_parameters}'


class Config:
    def __init__(self, path="./config/config.yml"):
        os.makedirs('./config', exist_ok=True)
        with open(path, 'r') as config:
            self.__config = yaml.safe_load(config)

    def get_pushover_user(self):
        """
        Gets the Pushover user key.
        :return: Returns the Pushover user key as a string.
        """
        return self.__config['scraper']['settings']['pushover']['user']

    def get_pushover_token(self):
        """
        Gets the Pushover API token.
        :return: Returns the Pushover API token as a string.
        """
        return self.__config['scraper']['settings']['pushover']['token']

    def get_queries(self):
        """
        Returns search queries as a list of SearchQuery objects.
        """
        search_queries = self.__config['scraper']['query']
        results = [SearchQuery(query) for query in search_queries]
        return results

    def get_scan_interval(self) -> int:
        """
        Gets the time in seconds between scanning ads.
        :return: Returns the time in seconds.
        """
        return int(self.__config['scraper']['settings']['scan_interval'])