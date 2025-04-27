BOT_NAME = 'hotel_scraper'

SPIDER_MODULES = ['app.scraper.spiders']
NEWSPIDER_MODULE = 'app.scraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website
DOWNLOAD_DELAY = 3

# Enable Selenium middleware
DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800
}

# Selenium settings
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = None  # Will use webdriver-manager
SELENIUM_DRIVER_ARGUMENTS = [
    '--headless=new',
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--window-size=1920,1080',
    '--disable-blink-features=AutomationControlled'
]

# Configure item pipelines
ITEM_PIPELINES = {
    'app.scraper.pipelines.HotelScraperPipeline': 300,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncio.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Custom settings for different sites
CUSTOM_SETTINGS = {
    'booking.com': {
        'DOWNLOAD_DELAY': 2,  # Be more gentle with Booking.com
        'COOKIES_ENABLED': True,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    },
    'agoda.com': {
        'DOWNLOAD_DELAY': 2,  # Be more gentle with Agoda
        'COOKIES_ENABLED': True,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
}

# Enable the pipeline
ITEM_PIPELINES_ENABLED = True

# Configure the feed exporter
FEED_FORMAT = 'json'
FEED_URI = 'stdout:'
FEED_EXPORT_ENCODING = 'utf-8'
FEED_EXPORT_INDENT = 2

# Configure the crawler
CRAWLER_PROCESS = {
    'LOG_LEVEL': 'DEBUG',
    'LOG_FORMAT': '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
}

# Configure the pipeline
PIPELINE = {
    'LOG_LEVEL': 'DEBUG',
    'LOG_FORMAT': '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
}

# Configure the feed exporter
FEED_EXPORT_FIELDS = [
    'hotel_name',
    'price',
    'rating',
    'image',
    'booking_url',
    'source'
] 