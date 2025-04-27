import scrapy
from scrapy.http import HtmlResponse
from typing import Optional, Callable
from datetime import datetime, date, timedelta
from urllib.parse import quote

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BookingSpider(scrapy.Spider):
    name = 'booking'
    
    def __init__(self, city: Optional[str] = None,
                 check_in: Optional[str] = None,
                 check_out: Optional[str] = None,
                 adults: int = 2,
                 children: int = 0,
                 rooms: int = 1,
                 min_price: Optional[float] = None, 
                 max_price: Optional[float] = None, 
                 star_rating: Optional[int] = None,
                 collect_item: Optional[Callable] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default values for required parameters
        self.city = city or "Dhaka"
        
        # # Handle dates
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

        # # Format the Booking.com search URL
        self.start_url = (
            f'https://www.booking.com/searchresults.html'
            f'?ss={quote(self.city)}'
            f'&checkin={self.check_in.strftime("%Y-%m-%d")}'
            f'&checkout={self.check_out.strftime("%Y-%m-%d")}'
            f'&group_adults={self.adults}'
            f'&no_rooms={self.rooms}'
            f'&group_children={self.children}'
        )
        
        # # Add price and rating filters if specified
        if self.min_price is not None and self.max_price is not None:
            self.start_url += f'&nflt=price%3DBDT-{int(self.min_price)}-{int(self.max_price)}-1'
        if self.star_rating is not None:
            self.start_url += f'%3Bclass%3D{self.star_rating}'

        options = Options()
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def start_requests(self):
        self.driver.get(self.start_url)

        # Wait for the page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="property-card"]'))
        )

        # Debug: Try to find elements using Selenium first
        try:
            html = self.driver.page_source

            # # Pass it to Scrapy-style parser
            response = HtmlResponse(url=self.start_url, body=html, encoding='utf-8')
            
            # # Debug: Check if the selector exists
            hotel_cards = response.css('[data-testid="property-card"]')
            print(f"Found {len(hotel_cards)} hotels using Scrapy")
            
            if not hotel_cards:
                print("No hotel cards found by Scrapy")
                return
                
            # Process each hotel card
            for hotel in hotel_cards:
                try:
                    name = hotel.css('[data-testid="title"]::text').get()
                    price_text = hotel.css('[data-testid="price-and-discounted-price"]::text').get()
                    rating = len(hotel.css('[data-testid="rating-stars"] span').getall())
                    image = hotel.css('[data-testid="image"]::attr(src)').get()
                    booking_url = hotel.css('[data-testid="title-link"]::attr(href)').get()
                    
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
                        'source': 'booking.com'
                    }

                    print(item, "item")

                    self.collect_item(item)

                except Exception as e:
                    print(f"Error processing hotel: {str(e)}")
                    continue

            yield None

        except Exception as e:
            print(f"Error finding hotel cards with Selenium: {str(e)}")
        finally:
            self.driver.quit()

    