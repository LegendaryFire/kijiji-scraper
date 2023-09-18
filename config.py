from constants import API_SEARCH_ENDPOINT
from urllib import parse
import yaml


class SearchQuery:
    def __init__(self, locationId, categoryId, search, page, size, nickname):
        self.__locationId = locationId
        self.__categoryId = categoryId
        self.__search = search
        self.__page = page
        self.__size = size
        self.__nickname = nickname

    def get_location(self):
        return self.__locationId

    def get_category(self):
        return self.__categoryId

    def get_search(self):
        return self.__search

    def get_page(self):
        return self.__page

    def get_size(self):
        return self.__size

    def get_nickname(self):
        return self.__nickname

    def get_url(self):
        url_parameters = parse.urlencode({
            'locationId': self.__locationId,
            'categoryId': self.__categoryId,
            'q': self.__search,
            'page': self.__page,
            'size': self.__size,
        })
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
        results = []
        for query in search_queries:
            results.append(SearchQuery(query.get('locationId'),
                                       query.get('categoryId'),
                                       query.get('q'),
                                       query.get('page'),
                                       query.get('size'),
                                       query.get('search')
                                       )
                           )
        return results

