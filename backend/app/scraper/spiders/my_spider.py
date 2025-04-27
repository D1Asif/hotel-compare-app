import scrapy

class MySpider(scrapy.Spider):
    name = "my_spider"

    def __init__(self, query=None, collect_item=None, **kwargs):
        super().__init__(**kwargs)
        self.query = query
        self.collect_item = collect_item

    def start_requests(self):
        url = f"https://quotes.toscrape.com/page/1/"
        yield scrapy.Request(url, callback=self.parse)

    # start_urls = [
    #     "https://quotes.toscrape.com/page/1/",
    # ]

    def parse(self, response):
        for card in response.css(".quote"):
            item = {
                "quote_text": card.css("span.text::text").get(),
                "link": card.css("small::text").get(),
            }

            if self.collect_item:
                self.collect_item(item)
