# novelupdates-downloader
Scrapy novelupdates scraper to download chapters from a novel directory

requires Scrapy 1.7.3

How to scrape : scrapy crawl novel -a directory='novel directory here' -a span='start-end' -a novelName='name of the directory
for your chapters'

Requires the chapters to be integers in the novel directory.
Won't download if the chapter website uses something other than the <p> tag (Most use it) for their chapter text. 
