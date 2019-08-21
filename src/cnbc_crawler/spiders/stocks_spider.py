# this is the scrapy web crawler collecting data from cnbc.com
# the data is stored in a local mongoDB instance for further processing/analyis

import scrapy
import pymongo
import datetime

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "kddm"


class Article(scrapy.Item):
    title = scrapy.Field()
    timestamp = scrapy.Field()


class StockMention(scrapy.Item):
    symbol = scrapy.Field()
    timestamp = scrapy.Field()
    count = scrapy.Field()


class StocksSpider(scrapy.Spider):
    name = "stocks"
    numberPages = 294
    baseUrl = 'https://www.cnbc.com/technology/'

    def start_requests(self):
        yield scrapy.Request(self.baseUrl, callback=self.init)

    def init(self, response):
        connection = pymongo.MongoClient(
            MONGODB_SERVER,
            MONGODB_PORT
        )
        db = connection[MONGODB_DB]
        self.articleCollection = db['articles']
        self.mentionCollection = db['mentions']

        self.logger.warning('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        self.logger.warning('number pages: ' + str(self.numberPages))
        # self.numberPages = response.css('span.pageCount a::attr(page)').extract_first()
        self.logger.warning('number pages: ' + str(self.numberPages))
        for pagenum in range(self.numberPages):
            yield scrapy.Request(self.baseUrl + '?page=' + str(pagenum + 1), self.parse_page)

    def parse(self):
        self.logger.warning('are here')
        for pagenum in range(self.numberPages):
            yield scrapy.Request(self.baseUrl + '?page=' + str(pagenum + 1), self.parse_page)
            # filename = 'quotes-%s.html' % page

    def parse_page(self, response):
        # follow links to article pages
        for href in response.css('div.headline a::attr(href)'):
            yield response.follow(href, self.parse_article)

    def parse_article(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        article = Article()
        article['title'] = extract_with_css('h1.title::text')
        article['timestamp'] = extract_with_css('time.datestamp::attr(datetime)')

        stockSymbols = response.xpath('//a[contains(@href, "quotes")]/@href').re('.*\\?symbol\\=\\s*([A-Z]*)')
        stockSymbols = set(stockSymbols)  # to make entries unique
        for symbol in stockSymbols:
            isoDate = datetime.datetime.strptime(article['timestamp'],
                                                 "%Y-%m-%dT%H:%M:%S%z").date().isoformat()

            mentionQuery = {"timestamp": isoDate, "symbol": symbol}
            mentionInDb = self.mentionCollection.count_documents(mentionQuery)
            if mentionInDb == 1:
                self.mentionCollection.update_one(mentionQuery, {"$inc": {"count": 1}})
            else:
                mention = StockMention()
                mention['symbol'] = symbol
                mention['count'] = 1
                # 2018-11-21T02:41:43-0500
                mention['timestamp'] = isoDate
                self.mentionCollection.insert(dict(mention))

        yield article
