import logging
from datetime import datetime, timezone
import requests
from constants import API_REQUEST_HEADERS
import xmltodict
from database import Ad


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
                if isinstance(json_data, list):
                    for json_ad in json_data:
                        ad_list.append(json_ad)
                elif isinstance(json_data, dict):
                    ad_list.append(json_data)
                else:
                    logging.warning("No search results returned.")
                return ad_list
        else:
            logging.warning(f"Unable to get search results. Status code {resp.status_code}.")
            return None

    @staticmethod
    def parse_ad(data) -> Ad:
        """
        Parses JSON ad data into an Ad object.
        :param data: The JSON ad data.
        :return: Returns an Ad object.
        """
        id = data.get('@id')
        is_business = id[0] == 'm'
        title = data.get('ad:title')
        description = data.get('ad:description')
        type = data.get('ad:ad-type').get('ad:value').capitalize()
        price = "Wanted" if type == "Wanted" \
            else "Offered" if data.get('ad:price') is None and type == "Offered" \
            else "Please Contact" if data.get('ad:price').get('types:amount') is None \
            else data.get('ad:price').get('types:amount')
        user_id = data.get('ad:user-id')
        datetime_scraped = datetime.now(timezone.utc)
        datetime_creation = datetime.strptime(data.get('ad:creation-date-time'), '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc)
        datetime_start = datetime.strptime(data.get('ad:start-date-time'), '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc)
        datetime_end = datetime.strptime(data.get('ad:end-date-time'), '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc) if data.get('ad:end-date-time') is not None else None
        phone = data.get('ad:phone')
        location = data.get('loc:locations').get('loc:location') if data.get('loc:locations') is not None else None
        if isinstance(location, list):
            location = location[0].get['loc:localized-name']
        elif isinstance(location, dict):
            location = location.get('loc:localized-name')
        image = data.get('pic:pictures').get('pic:picture') if data.get('pic:pictures') is not None else None
        if isinstance(image, list):
            image = image[0].get('pic:link')
        elif isinstance(image, dict):
            image = image.get('pic:link')
        if image is not None:
            for i in range(len(image)):
                if image[i].get('@rel') == 'extraLarge':
                    image = image[i].get('@href')

        ad = Ad(id=id,
                is_business=is_business,
                title=title,
                description=description,
                type=type,
                price=price,
                location=location,
                phone=phone,
                user_id=user_id,
                datetime_scraped=datetime_scraped,
                datetime_creation=datetime_creation,
                datetime_start=datetime_start,
                datetime_end=datetime_end,
                image=image
                )

        return ad

