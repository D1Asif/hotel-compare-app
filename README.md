# Hotel Compare App

A full-stack application that allows users to compare hotel prices across different booking platforms (Booking.com and Agoda) and save their favorite deals.

## Project Overview

The Hotel Compare App is designed to help users find the best hotel deals by:
- Searching hotels across multiple booking platforms
- Comparing prices in real-time
- Saving favorite hotels for later reference
- Providing direct booking links to the best deals

## Features

- **Price Comparison**
  - Real-time price comparison between Booking.com and Agoda
  - Best deal highlighting
  - Price display in BDT (Bangladesh Taka)

- **User Features**
  - User authentication
  - Hotel search with filters
  - Bookmark management
  - Responsive design

- **Technical Features**
  - Web scraping for real-time prices
  - JWT authentication
  - RESTful API
  - Modern UI with Tailwind CSS

## Project Structure

The project is divided into two main parts:

1. **Frontend** (`/frontend`)
   - React-based web application
   - Modern UI with Tailwind CSS
   - User authentication and protected routes
   - Real-time price comparison interface

2. **Backend** (`/backend`)
   - FastAPI-based REST API
   - Web scraping with Scrapy
   - PostgreSQL database with Prisma ORM
   - JWT authentication

## Getting Started

For detailed setup instructions, please refer to the respective README files:

- [Frontend Setup Guide](frontend/README.md)
- [Backend Setup Guide](backend/README.md)

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd hotel-compare-app
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

3. Set up the frontend:
```bash
cd frontend
npm install
npm start
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Tech Stack

### Frontend
- React
- React Router
- Tailwind CSS
- Context API
- Fetch API

### Backend
- FastAPI
- Scrapy
- PostgreSQL
- Prisma ORM
- JWT Authentication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 