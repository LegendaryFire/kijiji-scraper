import time
import database
import scraper as sc
import config

config = config.Config()
scraper = sc.Scraper()
database = database.Database()

while True:
    for query in config.get_queries():
        results = scraper.search(query.build_url())
        for ad in results:
            exists = database.exists(ad)
            if exists is False:
                saved_ad = database.save_ad(ad)
            else:
                # Check for changes.
                pass
    time.sleep(config.get_scan_interval())
