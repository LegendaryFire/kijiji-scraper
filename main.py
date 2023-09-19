import database
import scraper as sc
import config

config = config.Config()
search_queries = config.get_queries()
scraper = sc.Scraper()

database = database.Database()

for query in search_queries:
    results = scraper.search(query.build_url())
    for ad in results:
        exists = database.exists(ad)
        if exists is False:
            saved_ad = database.save_ad(ad)
        else:
            # Check for changes.
            pass
