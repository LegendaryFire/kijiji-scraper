import logging
from PIL import Image

from database import Ad
import requests


class Pushover:
    def __init__(self, token, user):
        self.__token = token
        self.__user = user

    def send_notification(self, ad: Ad, changes=None) -> bool:
        title = ad.title
        message = f'<a href="https://www.kijiji.ca/v-view-details.html?adId={ad.id}">Click here to view.</a>\n\n' \
                  f"<b>Price:</b> {ad.price}\n" \
                  f"<b>Description:</b> {ad.description}\n"
        data = {
            "token": self.__token,
            "user": self.__user,
            "html": int(True),
            "message": message,
            "title": title,
        }
        files = {
            "attachment": ("image.jpg", requests.get(ad.image, stream=True).raw, "image/jpeg")
        }
        resp = requests.post("https://api.pushover.net/1/messages.json", data=data, files=files)
        if resp.status_code == 200:
            return True
        else:
            logging.warning(f"Could not send Pushover notification. Status code {resp.status_code}.")
            return False

