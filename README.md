# Hotel Compare App

A web application that helps users find the best hotel deals by comparing prices across different booking platforms.

## Project Overview

This project consists of two main components:
- **Backend**: A FastAPI-based service that handles hotel data scraping, comparison, and API endpoints
- **Frontend**: A React application that provides the user interface for searching and comparing hotels

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd hotel-compare-app
```

2. Set up the backend:
[Backend Documentation](backend/README.md) - Detailed backend setup and API documentation

3. Set up the frontend: (yet to be implemented)
```bash
cd frontend
npm install
npm run dev
```

4. Access the application:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Project Structure

```
hotel-compare-app/
├── backend/           # FastAPI backend service
│   ├── app/          # Application code
│   ├── prisma/       # Database schema
│   └── README.md     # Backend documentation
├── frontend/         # React frontend application
└── README.md         # This file
```

## Features

- Search hotels across multiple booking platforms
- Compare prices from different sources
- User authentication and authorization
- Bookmark favorite hotels
- Real-time price comparison
- Responsive design

## Documentation

- [Backend Documentation](backend/README.md) - Detailed backend setup and API documentation
- [Frontend Documentation](frontend/README.md) - Frontend setup and development guide

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 