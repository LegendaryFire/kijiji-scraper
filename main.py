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
        for ad in results:
            ad = scraper.parse_ad(ad)
            exists = database.exists(ad)
            if exists is False:
                database.save_ad(ad)
                if query.send_notifications():
                    if ad.is_business:
                        if query.include_business():
                            pushover.send_notification(ad)
                    else:
                        pushover.send_notification(ad)
            else:
                # Check for changes.
                changes = database.compare(ad, True)
                if len(changes) > 0:
                    # Notify user of changes made to ad. Bumped, price change, etc.
                    pass
    time.sleep(config.get_scan_interval())
