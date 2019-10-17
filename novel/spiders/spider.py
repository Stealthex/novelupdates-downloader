#!/usr/bin/env python3

from scrapy.exceptions import CloseSpider
import scrapy
import time
import os


class chapterSpider(scrapy.Spider):
    name = "novel"
    chapterCount = 0
    firstParse = True

    def __init__(self, category=None, *args, **kwargs):
        super(chapterSpider, self).__init__(*args, **kwargs)
        self.start_urls = [self.directory]
        self.start, self.end = [int(x) for x in self.span.split("-")]
        self.chapterAmount = self.end - self.start
        self.dName = self.novelName
        self.path = os.getcwd() + '/' + self.dName
        os.mkdir(self.path)
        super().__init__(**kwargs)

    def parse(self, response):
        if self.firstParse:
            latestChapter = response.xpath(
                ".//a[@class='chp-release']/@title").get()
            chapterDifference = int(latestChapter[1:]) - self.end
            pgNumber = int(chapterDifference / 15 + 1)
            startPg = "?pg=" + str(pgNumber)
            start_page_link = response.urljoin(startPg)
            self.firstParse = False
            yield scrapy.Request(url=start_page_link, callback=self.parse)
        else:
            chapterLink = response.xpath(
                ".//a[@class='chp-release']/@href").getall()
            cNumber = response.xpath(
                ".//a[@class='chp-release']/@title").getall()
            for number, link in zip(cNumber, chapterLink):
                numberInt = int(number[1:])
                if int(numberInt) in range(self.start, self.end):
                    yield scrapy.Request(url='https:' + link, callback=self.parseChapter, meta={'chapter': numberInt})
                    time.sleep(1)

            next_page = response.xpath(
                "//div[@class='digg_pagination']/a[@rel='next']/@href").get()
            if next_page is not None and self.chapterCount != self.chapterAmount:
                next_page_link = response.urljoin(next_page)
                time.sleep(1.5)
                yield scrapy.Request(url=next_page_link, callback=self.parse)

    def parseChapter(self, response):
        self.chapterCount += 1
        number = response.meta.get('chapter')
        f = open(self.path + '/chapter' + str(number) + '.txt', 'w+')
        for div in response.xpath(".//div"):
            if 10 <= len(div.xpath('./p')):
                for sentence in div.xpath("./p"):
                    text = sentence.xpath('.//text()').get()
                    if isinstance(
                            text, str):  # test to make sure text is not NoneType
                        f.write(text + '\n\n')
        f.close()
        if self.chapterCount == self.chapterAmount:
            raise CloseSpider('chapters download complete')
