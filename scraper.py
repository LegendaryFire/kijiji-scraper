import requests
from constants import API_REQUEST_HEADERS


class Scraper:
    def __init__(self):
        self.__session = requests.session()

    def scrape(self, url):
        resp = self.__session.get(url, headers=API_REQUEST_HEADERS)
