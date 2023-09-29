import time
import database
import scraper as sc
import config
import notifications

config = config.Config()
scraper = sc.Scraper()
database = database.Database()
pushover = notifications.Pushover(config.get_pushover_token(), config.get_pushover_user())

while True:
    for query in config.get_queries():
        results = scraper.search(query.build_url())
        if results:  # Make sure there are results to iterate through.
            for ad in results:
                ad = scraper.parse_ad(ad)
                exists = database.exists(ad)
                if not exists:
                    # This is an ad we've never seen before.
                    database.save_ad(ad)
                    if query.send_notifications():
                        if (ad.is_business and query.include_business()) or (not ad.is_business):
                            pushover.send_notification(ad)
                else:
                    # We've seen this ad before, let's look for any changes.
                    changes = database.compare(ad, True)
                    if len(changes) > 0:
                        if query.send_notifications():
                            if (ad.is_business and query.include_business()) or (not ad.is_business):
                                pushover.send_notification(ad, changes)

    time.sleep(config.get_scan_interval())
