from crochet import setup, wait_for
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from app.scraper.spiders.booking_spider import BookingSpider
from app.scraper.spiders.agoda_spider import AgodaSpider
from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.scraper.spiders.my_spider import MySpider
from twisted.internet.defer import DeferredList

setup()

class ScrapySearchService:
    def __init__(self):
        self.runner = CrawlerRunner(get_project_settings())
        self.items = []

    @wait_for(timeout=120.0)  # Increased timeout to 120 seconds
    def run_spider(self, search_params: Dict[str, Any]):
        self.items = []  # Initialize empty list

        def collect_item(item):
            if item is not None:  # Only append if item is not None
                self.items.append(item)

        # Get default dates if not provided
        tomorrow = datetime.now() + timedelta(days=1)
        day_after = tomorrow + timedelta(days=1)
        default_check_in = tomorrow.strftime('%Y-%m-%d')
        default_check_out = day_after.strftime('%Y-%m-%d')

        # Run Booking.com spider with optional parameters
        booking_deferred = self.runner.crawl(
            BookingSpider,
            city=search_params.get('city', "Dhaka"),
            check_in=search_params.get('check_in', default_check_in),
            check_out=search_params.get('check_out', default_check_out),
            adults=search_params.get('adults', 2),
            children=search_params.get('children', 0),
            rooms=search_params.get('rooms', 1),
            min_price=search_params.get('min_price', 0),
            max_price=search_params.get('max_price', 100000),
            star_rating=search_params.get('star_rating', 5),
            collect_item=collect_item
        )

        # Run Agoda spider with optional parameters
        agoda_deferred = self.runner.crawl(
            AgodaSpider,
            city=search_params.get('city', 'Dhaka'),
            check_in=search_params.get('check_in', default_check_in),
            check_out=search_params.get('check_out', default_check_out),
            adults=search_params.get('adults', 2),
            children=search_params.get('children', 0),
            rooms=search_params.get('rooms', 1),
            min_price=search_params.get('min_price', 0),
            max_price=search_params.get('max_price', 100000),
            star_rating=search_params.get('star_rating', 5),
            collect_item=collect_item
        )

        return DeferredList([booking_deferred, agoda_deferred])

    def get_items(self):
        return self.items # Return empty list if no items found