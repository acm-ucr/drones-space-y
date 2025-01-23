from icrawler.builtin import BaiduImageCrawler, BingImageCrawler, GoogleImageCrawler
import os
from datetime import date, datetime

storage = { "backend": "FileSystem", 
           "root_dir": "/Users/pratheeksunilkumar/TrafficConeDetection/.venv/negative" # Specify your desired directory here 
}

filters = dict(
    date=((2010, 1, 1), (2025, 11, 30)))


#Google Crawler:
# google_crawler = GoogleImageCrawler(storage={'root_dir': 'images4'})

# google_crawler.crawl(keyword='traffic cone', filters=filters, max_num=1000, 
#                      min_size=(200,200), max_size=(3000,3000))


#Bing Crawler:
bing_crawler = BingImageCrawler(
    parser_threads=2,
    downloader_threads=4,
    storage=storage
)

for keyword in ["asphalt", "pavement", "people", "people on road", "people on pavement", "tar", "roads", "highway", "freeway"]:
    bing_crawler.crawl(
        keyword=keyword,
        max_num=1000,
        file_idx_offset='auto'
    )


