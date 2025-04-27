# Hotel Compare App

A web application that compares hotel prices across different booking platforms to help users find the best deals.

## Features

- Search hotels across multiple booking platforms
- Compare prices from different sources
- User authentication and authorization
- Bookmark favorite hotels
- Real-time price comparison
- Responsive design

## Tech Stack

### Backend
- FastAPI (Python web framework)
- Prisma (ORM)
- Scrapy (Web scraping)
- Selenium (Dynamic content scraping)
- JWT Authentication
- PostgreSQL (Database)

### Frontend
- React
- TypeScript
- Tailwind CSS
- React Query
- React Router

## Project Structure

```
hotel-compare-app/
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
- Node.js 14+
- PostgreSQL
- Chrome/Chromium (for Selenium)

### Backend Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the database:
```bash
python init_prisma.py
```

4. Start the backend server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

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