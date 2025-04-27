import scrapy
from scrapy.http import HtmlResponse
from typing import Optional, Callable
from datetime import datetime, date, timedelta
from urllib.parse import quote, urlparse, parse_qs

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AgodaSpider(scrapy.Spider):
    name = 'agoda'
    
    def __init__(self, city: Optional[str] = None,
                 check_in: Optional[str] = None,
                 check_out: Optional[str] = None,
                 adults: int = 2,
                 children: int = 0,
                 rooms: int = 1,
                 min_price: Optional[float] = 0, 
                 max_price: Optional[float] = 50000, 
                 star_rating: Optional[int] = 5,
                 collect_item: Optional[Callable] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default values for required parameters
        self.city = city or "Dhaka"  # Default city
        
        # Handle dates
        if check_in:
            try:
                self.check_in = datetime.strptime(check_in, '%Y-%m-%d').date()
            except ValueError:
                # If date parsing fails, use default
                self.check_in = (datetime.now() + timedelta(days=1)).date()
        else:
            self.check_in = (datetime.now() + timedelta(days=1)).date()
            
        if check_out:
            try:
                self.check_out = datetime.strptime(check_out, '%Y-%m-%d').date()
            except ValueError:
                # If date parsing fails, use default
                self.check_out = (self.check_in + timedelta(days=1))
        else:
            self.check_out = (self.check_in + timedelta(days=1))
            
        self.adults = adults
        self.children = children
        self.rooms = rooms
        self.min_price = min_price
        self.max_price = max_price
        self.star_rating = star_rating
        self.collect_item = collect_item
        
        # Format the Agoda search URL
        self.start_url = (
            f'https://www.agoda.com/search?'
            f'&checkIn={self.check_in.strftime("%Y-%m-%d")}'
            f'&checkOut={self.check_out.strftime("%Y-%m-%d")}'
            f'&adults={self.adults}'
            f'&children={self.children}'
            f'&rooms={self.rooms}'
            f'&currency=BDT'
        )
        
        # Add price and rating filters if specified
        if self.min_price is not None and self.max_price is not None:
            self.start_url += f'&PriceFrom={int(self.min_price)}&PriceTo={int(self.max_price)}'
        if self.star_rating is not None:
            self.start_url += f'&hotelStarRating={self.star_rating}'

        options = Options()
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def start_requests(self):
        self.driver.get("https://www.agoda.com/")

        time.sleep(3)  # Give it some time to load (you can make this smarter with WebDriverWait)

        # 3. Find the search field and type city name
        search_field = self.driver.find_element(By.CSS_SELECTOR, 'input[data-selenium="textInput"]')
        search_field.send_keys(self.city)  # You can change 'Dhaka' to any city
        time.sleep(1)

        
        # Simulate pressing down arrow and enter to select first result
        suggestion = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li[data-selenium="suggestion-category-name"]'))
        )

        suggestion.click()
        time.sleep(1)

        checkin_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-element-name="check-in-box"]')
        checkin_box.click()
        time.sleep(1)
        

        # 4. Press Enter key to search
        search_button = self.driver.find_element(By.CSS_SELECTOR, 'button[data-selenium="searchButton"]')
        search_button.click()

        # 5. Wait for page to load (again, better with WebDriverWait)
        time.sleep(5)

        # 6. Get current URL
        current_url = self.driver.current_url
        print("Current URL:", current_url)

        # 7. Extract city param from URL
        parsed_url = urlparse(current_url)
        query_params = parse_qs(parsed_url.query)

        # Some Agoda URLs have 'city' param, some have other structure
        self.city_code = query_params.get('city', '1390')[0]
        print("City search param:", self.city_code)

        self.start_url = self.start_url + f'&city={self.city_code}'

        self.driver.get(self.start_url)

        time.sleep(5)

        # Debug: Try to find elements using Selenium first
        try:
            # Get the entire page source
            html = self.driver.page_source

            # Pass it to Scrapy-style parser
            response = HtmlResponse(url=self.start_url, body=html, encoding='utf-8')
            
            # Debug: Check if the selector exists
            container = response.css('div#sort-bar + div')
            hotel_cards = container.css('[data-selenium="hotel-item"]')
            print(f"Found {len(hotel_cards)} hotels using Scrapy")
            
            if not hotel_cards:
                print("No hotel cards found by Scrapy")
                return
                
            # Process each hotel card
            for hotel in hotel_cards:
                try:
                    name = hotel.css('[data-selenium="hotel-name"]::text').get()
                    price_text = hotel.css('[data-selenium="display-price"]::text').get()
                    rating = len(hotel.css('[data-testid="rating-container"] svg').getall())
                    image = hotel.css('[data-element-name="ssrweb-mainphoto"] img::attr(src)').get()
                    booking_url = hotel.css('[data-element-name="property-card-content"]::attr(href)').get()
                    
                    
                    # Convert price to float
                    price = float(price_text.replace('BDT', '').replace(',', '').strip())
                    
                    # Apply filters
                    if (self.min_price and price < self.min_price) or \
                       (self.max_price and price > self.max_price) or \
                       (self.star_rating and rating != self.star_rating):
                        continue
                    
                    # Make sure booking_url is absolute
                    booking_url = response.urljoin(booking_url)
                    
                    item = {
                        'hotel_name': name,
                        'price': price,
                        'rating': rating,
                        'image': image,
                        'booking_url': booking_url,
                        'source': 'agoda'
                    }

                    print(item)

                    if self.collect_item:
                        self.collect_item(item)
                except Exception as e:
                    print(f"Error processing hotel: {str(e)}")
                    continue

            yield None

        except Exception as e:
            print(f"Error finding hotel cards with Selenium: {str(e)}")
        finally:
            self.driver.quit()
            

