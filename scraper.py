import logging
import requests
from constants import API_REQUEST_HEADERS
import xmltodict


class Scraper:
    def __init__(self):
        self.__session = requests.session()

    def search(self, url):
        """
        Gets all ads for a given search query.
        :param url: The URL of the search query.
        :return: Returns ad data as a list of JSON objects.
        """
        resp = self.__session.get(url, headers=API_REQUEST_HEADERS)
        if resp.status_code == 200:
            json_data = xmltodict.parse(resp.text)
            if 'ad:ads' in json_data.keys():
                json_data = json_data['ad:ads'].get('ad:ad')
                ad_list = []
                for json_ad in json_data:
                    ad_list.append(json_ad)
                return ad_list
        else:
            logging.warning(f"Unable to get search results. Status code {resp.status_code}.")
            return None


