import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes_xpath"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.xpath('//div//div//div//div'):
            yield {
                'text': quote.xpath("//span[contains(@class,'text')]/text()").get(),
                'author': quote.xpath("//small[contains(@class,'author')]/text()").get(),
                'tags': quote.xpath("//meta[contains(@class,'keywords')]/@content").get().split(",")
            }
        next_page = response.xpath("//li[contains(@class, 'next')]//a/@href").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)  # can use follow method instead as  short cut 9see snipet below
            yield scrapy.Request(next_page, callback=self.parse)

# TO Follow example snipet
# next_page = response.css('li.next a::attr(href)').get()
#             if next_page is not None:
#                 yield response.follow(next_page, callback=self.parse)


# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#
#     def start_requests(self):
#         urls = [
#                 'http://quotes.toscrape.com/page/1/',
#                 'http://quotes.toscrape.com/page/2/',
#             ]
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse)
#
#     def parse(self, response):
#         page = response.url.split("/")[-2]
#         filename = 'quotes-%s.html' % page
#         with open(filename, 'wb') as f:
#             f.write(response.body)
#         self.log('Saved file %s' % filename)





# SHortcut to start request method used above

# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#             'http://quotes.toscrape.com/page/1/',
#             'http://quotes.toscrape.com/page/2/',
#     ]
#
#     def parse(self, response):
#         page = response.url.split("/")[-2]
#         filename = 'quotes-%s.html' % page
#         with open(filename, 'wb') as f:
#             f.write(response.body)