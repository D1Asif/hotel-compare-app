import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const HotelSearch = () => {
  const [city, setCity] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [rating, setRating] = useState('5');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [hotels, setHotels] = useState([]);
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    }
  }, [navigate]);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setHotels([]);

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const minPriceNum = minPrice ? parseInt(minPrice) : null;
      const maxPriceNum = maxPrice ? parseInt(maxPrice) : null;
      const ratingNum = rating ? parseInt(rating) : null;

      const response = await fetch('http://localhost:8000/search', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          city: city,
          min_price: minPriceNum,
          max_price: maxPriceNum,
          star_rating: ratingNum
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to fetch hotels');
      }

      const data = await response.json();
      if (data?.result) {
        setHotels(data.result);
      }
    } catch (err) {
      console.error('Search error:', err);
      if (err.message.includes('401')) {
        setError('Session expired. Please login again.');
        localStorage.removeItem('token');
        navigate('/login');
      } else {
        setError(err.message || 'Failed to fetch hotels');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleBookmark = async (hotel) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      // Find the best deal (lowest price)
      const bookingSource = hotel.sources.find(s => s.source === 'booking.com');
      const agodaSource = hotel.sources.find(s => s.source === 'agoda');
      const bestDeal = bookingSource && agodaSource 
        ? (bookingSource.price < agodaSource.price ? bookingSource : agodaSource)
        : bookingSource || agodaSource;

      if (!bestDeal) {
        throw new Error('No valid price found for bookmarking');
      }

      const bookmarkData = {
        hotel_name: hotel.hotel_name,
        image: bestDeal.image,
        price: bestDeal.price,
        rating: bestDeal.rating,
        booking_url: bestDeal.booking_url
      };

      const response = await fetch('http://localhost:8000/bookmarks', {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(bookmarkData)
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to bookmark hotel');
      }

      // Show success message
      setError('');
      alert('Hotel bookmarked successfully!');
    } catch (err) {
      console.error('Bookmark error:', err);
      if (err.message.includes('401')) {
        setError('Session expired. Please login again.');
        localStorage.removeItem('token');
        navigate('/login');
      } else {
        setError(err.message || 'Failed to bookmark hotel');
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-6 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Hotel Search</h1>
          <div className="flex space-x-4">
            <Link
              to="/bookmarks"
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              View Bookmarks
            </Link>
            <button
              onClick={() => {
                localStorage.removeItem('token');
                navigate('/login');
              }}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
            >
              Logout
            </button>
          </div>
        </div>

        <form onSubmit={handleSearch} className="bg-white shadow rounded-lg p-6 mb-8">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            <div>
              <label htmlFor="city" className="block text-sm font-medium text-gray-700">
                City
              </label>
              <input
                type="text"
                id="city"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                required
              />
            </div>
            <div>
              <label htmlFor="minPrice" className="block text-sm font-medium text-gray-700">
                Min Price (BDT)
              </label>
              <input
                type="number"
                id="minPrice"
                value={minPrice}
                onChange={(e) => setMinPrice(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                required
                min="0"
                placeholder="Enter minimum price in BDT"
              />
            </div>
            <div>
              <label htmlFor="maxPrice" className="block text-sm font-medium text-gray-700">
                Max Price (BDT)
              </label>
              <input
                type="number"
                id="maxPrice"
                value={maxPrice}
                onChange={(e) => setMaxPrice(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                required
                min="0"
                placeholder="Enter maximum price in BDT"
              />
            </div>
            <div>
              <label htmlFor="rating" className="block text-sm font-medium text-gray-700">
                Star Rating
              </label>
              <select
                id="rating"
                value={rating}
                onChange={(e) => setRating(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              >
                <option value="1">1 Star</option>
                <option value="2">2 Stars</option>
                <option value="3">3 Stars</option>
                <option value="4">4 Stars</option>
                <option value="5">5 Stars</option>
              </select>
            </div>
          </div>
          <div className="mt-6">
            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              {loading ? 'Searching...' : 'Search Hotels'}
            </button>
          </div>
        </form>

        {error && (
          <div className="rounded-md bg-red-50 p-4 mb-8">
            <div className="text-sm text-red-700">{error}</div>
          </div>
        )}

        {loading && (
          <div className="flex flex-col items-center justify-center h-64 space-y-4">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
            <p className="text-gray-600 text-center">
              Searching for hotels... This may take up to 2 minutes.
            </p>
          </div>
        )}

        {!loading && hotels.length > 0 && (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {hotels.map((hotel) => {
              const bookingSource = hotel.sources.find(s => s.source === 'booking.com');
              const agodaSource = hotel.sources.find(s => s.source === 'agoda');
              const bestDeal = bookingSource && agodaSource 
                ? (bookingSource.price < agodaSource.price ? bookingSource : agodaSource)
                : bookingSource || agodaSource;

              return (
                <div key={hotel.hotel_name} className="bg-white shadow rounded-lg overflow-hidden">
                  <img
                    src={bestDeal?.image || hotel.sources[0].image}
                    alt={hotel.hotel_name}
                    className="w-full h-48 object-cover"
                  />
                  <div className="p-4">
                    <h3 className="text-lg font-medium text-gray-900">{hotel.hotel_name}</h3>
                    <div className="mt-2 flex items-center">
                      <div className="flex items-center">
                        {[...Array(5)].map((_, i) => (
                          <svg
                            key={i}
                            className={`h-5 w-5 ${
                              i < (bestDeal?.rating || hotel.sources[0].rating) ? 'text-yellow-400' : 'text-gray-300'
                            }`}
                            fill="currentColor"
                            viewBox="0 0 20 20"
                          >
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                          </svg>
                        ))}
                      </div>
                      <span className="ml-2 text-sm text-gray-500">
                        {bestDeal?.rating || hotel.sources[0].rating} stars
                      </span>
                    </div>
                    <div className="mt-4 grid grid-cols-2 gap-4">
                      <div>
                        <h4 className="text-sm font-medium text-gray-500">Booking.com</h4>
                        {bookingSource ? (
                          <div className="mt-1">
                            <p className="text-lg font-medium text-gray-900">
                              BDT {bookingSource.price}
                            </p>
                            <a
                              href={bookingSource.booking_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-sm text-indigo-600 hover:text-indigo-500"
                            >
                              View Deal
                            </a>
                          </div>
                        ) : (
                          <p className="text-sm text-gray-500">Not available</p>
                        )}
                      </div>
                      <div>
                        <h4 className="text-sm font-medium text-gray-500">Agoda</h4>
                        {agodaSource ? (
                          <div className="mt-1">
                            <p className="text-lg font-medium text-gray-900">
                              BDT {agodaSource.price}
                            </p>
                            <a
                              href={agodaSource.booking_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-sm text-indigo-600 hover:text-indigo-500"
                            >
                              View Deal
                            </a>
                          </div>
                        ) : (
                          <p className="text-sm text-gray-500">Not available</p>
                        )}
                      </div>
                    </div>
                    {bookingSource && agodaSource && (
                      <div className="mt-4">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          Best Deal: {bestDeal.source}
                        </span>
                      </div>
                    )}
                    <div className="mt-4">
                      <button
                        onClick={() => handleBookmark(hotel)}
                        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                      >
                        Bookmark
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {!loading && hotels.length === 0 && !error && (
          <div className="text-center py-12">
            <h3 className="text-lg font-medium text-gray-900">No hotels found</h3>
            <p className="mt-2 text-sm text-gray-500">
              Try adjusting your search criteria
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default HotelSearch; 