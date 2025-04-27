from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

class SeleniumMiddleware:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')  # Use new headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)  # Increased wait time to 30 seconds

    def process_request(self, request, spider):
        if request.meta.get('selenium'):
            try:
                # Set a custom user agent
                self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                    "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                })
                
                self.driver.get(request.url)
                
                # Wait for the page to be fully loaded
                self.wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                
                # Additional wait for dynamic content
                time.sleep(5)
                
                # Check if we have the expected content
                if 'agoda.com' in request.url:
                    # Try to find hotel items
                    hotel_items = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-selenium="hotel-item"]')
                    if not hotel_items:
                        # If no items found, wait a bit longer and try again
                        time.sleep(5)
                        hotel_items = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-selenium="hotel-item"]')
                
                elif 'booking.com' in request.url:
                    # Try to find property cards
                    property_cards = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
                    if not property_cards:
                        # If no cards found, wait a bit longer and try again
                        time.sleep(5)
                        property_cards = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
                
                # Get the page source
                body = self.driver.page_source
                
                # Log the content for debugging
                spider.logger.info(f"Page source length: {len(body)}")
                if 'agoda.com' in request.url:
                    spider.logger.info(f"Found {len(hotel_items)} hotel items")
                elif 'booking.com' in request.url:
                    spider.logger.info(f"Found {len(property_cards)} property cards")
                
                return HtmlResponse(
                    self.driver.current_url,
                    body=body,
                    encoding='utf-8',
                    request=request
                )
                
            except Exception as e:
                spider.logger.error(f"Error in Selenium middleware: {e}")
                # Return whatever content we have
                body = self.driver.page_source
                return HtmlResponse(
                    self.driver.current_url,
                    body=body,
                    encoding='utf-8',
                    request=request
                )

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass 