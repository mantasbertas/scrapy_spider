# Scrapy Spider for Phone Data Extraction

This project contains a Scrapy spider that scrapes phone data from [productindetail.com](https://www.productindetail.com/) and stores the collected data in a MongoDB database running on localhost.

## Requirements:
- Python 3.6+
- Python libraries: Scrapy, pymongo
- MongoDB server on localhost

## Installation:

1. Clone the repository
2. Install dependencies 
   ```bash
   pip install -r requirements.txt

## Scraping:
After installation is complete can run the scraper from terminal with command:
```bash
scrapy crawl phones
```
or if you want to scrape a specific amount:

```bash
scrapy crawl phones -a limit=10
```

This will start the spider, which will scrape phone data from the target website and store it in the local MongoDB instance under the phone_data database in the phone_collection collection.


## Database Schema
- 'product_name'
- 'image_url'
- 'brand' 
- 'operating_system'
- 'display_size'
- 'dispaly_resolution'
- 'display_technology'
- 'display_resolution'

Each phone's data is stored as a separate document within the 'phones' collection in the 'phone_data' database
