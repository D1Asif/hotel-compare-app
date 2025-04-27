# Hotel Compare App - Backend

A FastAPI-based backend service that handles hotel data scraping, comparison, and API endpoints.

## Features

- Search hotels across multiple booking platforms
- Compare prices from different sources
- User authentication and authorization
- Bookmark favorite hotels
- Real-time price comparison

## Tech Stack

- FastAPI (Python web framework)
- Prisma (ORM)
- Scrapy (Web scraping)
- Selenium (Dynamic content scraping)
- JWT Authentication
- PostgreSQL (Database)

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── schemas.py           # Pydantic models
│   ├── auth.py             # Authentication logic
│   ├── database.py         # Database configuration
│   └── scraper/
│       ├── spiders/        # Scrapy spiders
│       ├── runner.py       # Scrapy runner service
│       └── settings.py     # Scrapy settings
├── prisma/
│   └── schema.prisma       # Database schema
├── comparator.py           # Hotel comparison logic
└── requirements.txt        # Python dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL
- Chrome/Chromium (for Selenium)

### Environment Setup

1. Create a `.env` file in the backend directory with the following variables:
```env
# Database
DATABASE_URL="postgresql://username:password@localhost:5432/hotel_compare"

# JWT
JWT_SECRET_KEY="your-secret-key"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Scraping
SCRAPING_INTERVAL=3600  # in seconds
MAX_CONCURRENT_REQUESTS=5

# Optional: Proxy settings if needed
# PROXY_URL="http://proxy:port"
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Database Setup

1. Create a PostgreSQL database:
```bash
createdb hotel_compare
```

2. Initialize Prisma and apply migrations:
```bash
python init_prisma.py
```

3. Verify database connection:
```bash
python -c "from app.database import prisma; prisma.connect()"
```

### Running the Application

1. Start the backend server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Documentation

### Authentication Endpoints

#### Register
- **POST** `/register`
- **Body**: `{ "email": string, "username": string, "password": string }`
- **Response**: User object with JWT tokens

#### Login
- **POST** `/login`
- **Body**: `{ "email": string, "password": string }`
- **Response**: JWT tokens

### Hotel Search

#### Search Hotels
- **GET** `/search`
- **Request Body**:
  ```json
  {
    "city": string,
    "check_in": date (YYYY-MM-DD),
    "check_out": date (YYYY-MM-DD),
    "adults": number,
    "children": number,
    "rooms": number,
    "min_price": number,
    "max_price": number,
    "star_rating": number
  }
  ```
- **Response**: List of hotels with price comparisons

### Bookmarks

#### Create Bookmark
- **POST** `/bookmarks`
- **Body**: `{ "hotel_name": string, "image": string, "price": number, "rating": number, "booking_url": string }`
- **Response**: Created bookmark object

#### Get User Bookmarks
- **GET** `/bookmarks`
- **Response**: List of user's bookmarks

#### Get Single Bookmark
- **GET** `/bookmarks/{bookmark_id}`
- **Response**: Bookmark object

## Scraping Implementation

The application uses Scrapy and Selenium to scrape hotel data from multiple booking platforms:

1. **Agoda Spider**: Scrapes hotel data from Agoda
   - Handles dynamic content loading
   - Extracts hotel details, prices, and ratings
   - Supports filtering by price and star rating

2. **Price Comparison**:
   - Groups hotels by name across different sources
   - Identifies the best deals
   - Sorts results by price

## Security Features

- JWT-based authentication
- Password hashing
- CORS middleware
- Input validation
- Rate limiting
- Error handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 