# Kijiji Scraper
Kijiji Scraper is a web crawler to provide a way to receive new listing notifications sooner than the ones from Kijiji which are only sent daily (once every 24-hours). This scraper also increases the functionality with bump and price change notifications. Notifications are sent using [Pushover](https://pushover.net/), and include a title, short description, image, price, phone number (if applicable) and a link to the ad.

## Configuration
The configuration file is found in the config directory, and is named _config.yml_. Crawled ads are saved into a SQLite database located in the config directory, and is named _default.db_. An example configuration file can be found below.
```
scraper:
  settings:
    scan_interval: 10
    pushover:
      token: YOUR_TOKEN
      user: YOUR_USER
  query:
    - search: Example Search
      include_business: False
      send_notification: True
      params:
        locationId: 0
        categoryId: 0
        page: 0
        size: 20
        q: My Search Terms
```
### Settings
The table below contains a brief description of each configuration variable.
|    Variable   |                          Description                         |
| ------------- | ------------------------------------------------------------ |
| scan_interval | How frequently each search query will be crawled in seconds. |
|     token     | The Pushover API token.                                      |
|     user      | The Pushover user key.                                       |

### Query
Each search query must have the following configuration variables, see below for a description of each. 
|       Variable      |                          Description                                        |
| ------------------- | --------------------------------------------------------------------------- |
|       search        | Internal search name, this can be whatever you like.                        |
|  include_business   | Whether listings from businesses will also be crawled or not.               |
|  send_notification  | Whether listings will be sent via Pushover for this search query.           |
|      locationId     | The location to search, found in the URL when searching Kijiji.             |
|      categoryId     | The category to search, found in the URL when searching Kijiji.             |
|        page         | The page of search results to crawl, zero being the first page.             |
|        size         | The number of search results per page.                                      |

Multiple search queries can be added to the configuration as seen below.
```
  query:
    - search: Search Number One
      include_business: False
      send_notification: True
      params:
        locationId: 0
        categoryId: 0
        page: 0
        size: 20
        q: Search Query One!
    - search: Search Number Two
      include_business: False
      send_notification: True
      params:
        locationId: 0
        categoryId: 0
        page: 0
        size: 20
        q: Search Query Two!
```
