import requests
from constants import API_REQUEST_HEADERS
import xmltodict
from datetime import datetime,timezone


class Ad:
    def __init__(self, data):
        self.__id = data.get('@id')
        self.__is_business = self.__id[0] == 'm'
        self.__title = data.get('ad:title')
        self.__description = data.get('ad:description')
        self.__type = data.get('ad:ad-type').get('ad:value').capitalize()
        self.__price = "Wanted" if self.__type == "Wanted" \
            else "Please Contact" if data.get('ad:price').get('types:amount') is None \
            else data.get('ad:price').get('types:amount')
        self.__user_id = data.get('ad:user-id')
        self.__datetime_scraped = datetime.now(timezone.utc)
        self.__datetime_creation = datetime.strptime(data.get('ad:creation-date-time'), '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc)
        self.__datetime_start = datetime.strptime(data.get('ad:start-date-time'), '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc)
        self.__datetime_end = datetime.strptime(data.get('ad:end-date-time'), '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc) if data.get('ad:end-date-time') is not None else None
        self.__image = None
        image = data.get('pic:pictures').get('pic:picture')
        if isinstance(image, list):
            self.__image = image[0].get('pic:link')
        elif isinstance(image, dict):
            self.__image = image.get('pic:link')
        if self.__image is not None:
            for i in range(len(self.__image)):
                if self.__image[i].get('@rel') == 'extraLarge':
                    self.__image = self.__image[i].get('@href')


class Scraper:
    def __init__(self):
        self.__session = requests.session()

    def scrape(self, url):
        resp = self.__session.get(url, headers=API_REQUEST_HEADERS)
        if resp.status_code == 200:
            raw_data = xmltodict.parse(resp.text)
            if 'ad:ads' in raw_data.keys():
                raw_data = raw_data['ad:ads'].get('ad:ad')
                ad_list = []
                for raw_ad in raw_data:
                    ad_list.append(Ad(raw_ad))
                return ad_list


