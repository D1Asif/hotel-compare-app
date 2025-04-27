# Hotel Compare App - Frontend

A React-based frontend application for comparing hotel prices across different booking platforms.

## Features

- **User Authentication**
  - Secure login and registration
  - JWT-based authentication
  - Protected routes

- **Hotel Search**
  - Search by city
  - Filter by price range (in BDT)
  - Filter by star rating (1-5 stars)
  - Real-time price comparison between Booking.com and Agoda
  - Best deal highlighting
  - Loading states with user feedback

- **Price Comparison**
  - Side-by-side price comparison
  - Best deal identification
  - Direct booking links
  - Price display in BDT

- **Bookmarks**
  - Save favorite hotels
  - View all bookmarks
  - Remove bookmarks
  - Automatic best deal selection for bookmarks

## Tech Stack

- **Core**
  - React 18
  - React Router v6
  - Context API for state management

- **Styling**
  - Tailwind CSS
  - Headless UI components
  - Responsive design

- **API Integration**
  - Fetch API for HTTP requests
  - JWT authentication
  - RESTful API integration

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Modern web browser

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hotel-compare-app/frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Create a `.env` file in the frontend directory:
```env
REACT_APP_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm start
# or
yarn start
```

The application will be available at http://localhost:3000

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable components
│   │   └── PrivateRoute.js
│   ├── context/       # React context providers
│   │   └── AuthContext.js
│   ├── pages/         # Page components
│   │   ├── Login.js
│   │   ├── Register.js
│   │   ├── HotelSearch.js
│   │   └── Bookmarks.js
│   ├── App.js         # Main application component
│   └── index.js       # Application entry point
├── public/            # Static files
└── package.json       # Project dependencies
```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Runs the test suite
- `npm eject` - Ejects from Create React App

## API Integration

The frontend integrates with the following backend endpoints:

- **Authentication**
  - POST `/login` - User login
  - POST `/register` - User registration

- **Hotel Search**
  - POST `/search` - Search hotels with filters

- **Bookmarks**
  - GET `/bookmarks` - Get user's bookmarks
  - POST `/bookmarks` - Create a new bookmark
  - DELETE `/bookmarks/{id}` - Delete a bookmark

## Error Handling

- Form validation
- API error handling
- Authentication error handling
- User-friendly error messages
- Loading states

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 