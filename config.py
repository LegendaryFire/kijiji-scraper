from constants import API_SEARCH_ENDPOINT
from urllib import parse
import yaml


class SearchQuery:
    def __init__(self, data):
        self.__data = data
        self.__search = self.__data.get('search')
        self.__params = self.__data.get('params')

    def get_search(self):
        """
        The name of the search.
        :return: Returns the name of the search.
        """
        return self.__search

    def build_url(self):
        """
        Builds the search URL for the given search query.
        :return: Returns the generated search URL.
        """
        url_parameters = parse.urlencode(self.__params)
        return f'{API_SEARCH_ENDPOINT}{url_parameters}'


class Config:
    def __init__(self, path="./config.yml"):
        with open(path, 'r') as config:
            self.__config = yaml.safe_load(config)

    def get_queries(self):
        """
        Returns search queries as a list of SearchQuery objects.
        """
        search_queries = self.__config['scraper']['query']
        results = [SearchQuery(query) for query in search_queries]
        return results

