from icrawler.builtin import BaiduImageCrawler, BingImageCrawler, GoogleImageCrawler

from datetime import date

#Resize images to camera size

#GOOGLE CRAWLER

filters = dict(
    date=((2010, 1, 1), (2025, 11, 30)))

google_crawler = GoogleImageCrawler(storage={'root_dir': 'images4'})

google_crawler.crawl(keyword='traffic cone', filters=filters, max_num=1000, 
                     min_size=(200,200), max_size=(3000,3000))


#BING CRAWLER
# bing_crawler = BingImageCrawler(downloader_threads=8,
#                                 storage={'root_dir': 'images3'})
# bing_crawler.crawl(keyword='traffic cone', filters=None, offset=0, max_num=1000)

