import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Bookmarks = () => {
  const [bookmarks, setBookmarks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchBookmarks = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('No authentication token found');
        }

        const response = await fetch('http://localhost:8000/bookmarks', {
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.detail || 'Failed to fetch bookmarks');
        }

        const data = await response.json();
        setBookmarks(data);
      } catch (err) {
        console.error('Fetch bookmarks error:', err);
        setError(err.message || 'Failed to fetch bookmarks');
      } finally {
        setLoading(false);
      }
    };

    fetchBookmarks();
  }, []);

  const handleRemoveBookmark = async (bookmarkId) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`http://localhost:8000/bookmarks/${bookmarkId}`, {
        method: 'DELETE',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to remove bookmark');
      }

      setBookmarks(bookmarks.filter(bookmark => bookmark.id !== bookmarkId));
    } catch (err) {
      console.error('Remove bookmark error:', err);
      setError(err.message || 'Failed to remove bookmark');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-6 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Bookmarks</h1>
          <Link
            to="/search"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
          >
            Back to Search
          </Link>
        </div>

        {error && (
          <div className="rounded-md bg-red-50 p-4 mb-8">
            <div className="text-sm text-red-700">{error}</div>
          </div>
        )}

        {loading && (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
          </div>
        )}

        {!loading && bookmarks.length > 0 && (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {bookmarks.map((bookmark) => (
              <div key={bookmark.id} className="bg-white shadow rounded-lg overflow-hidden">
                <img
                  src={bookmark.image}
                  alt={bookmark.hotel_name}
                  className="w-full h-48 object-cover"
                />
                <div className="p-4">
                  <h3 className="text-lg font-medium text-gray-900">{bookmark.hotel_name}</h3>
                  <div className="mt-2 flex items-center">
                    <div className="flex items-center">
                      {[...Array(5)].map((_, i) => (
                        <svg
                          key={i}
                          className={`h-5 w-5 ${
                            i < bookmark.rating ? 'text-yellow-400' : 'text-gray-300'
                          }`}
                          fill="currentColor"
                          viewBox="0 0 20 20"
                        >
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                      ))}
                    </div>
                    <span className="ml-2 text-sm text-gray-500">{bookmark.rating} stars</span>
                  </div>
                  <div className="mt-4">
                    <p className="text-lg font-medium text-gray-900">BDT {bookmark.price}</p>
                    <a
                      href={bookmark.booking_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-indigo-600 hover:text-indigo-500"
                    >
                      View Deal
                    </a>
                  </div>
                  <div className="mt-4">
                    <button
                      onClick={() => handleRemoveBookmark(bookmark.id)}
                      className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                    >
                      Remove Bookmark
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {!loading && bookmarks.length === 0 && (
          <div className="text-center py-12">
            <h3 className="text-lg font-medium text-gray-900">No bookmarks yet</h3>
            <p className="mt-2 text-sm text-gray-500">
              Start searching for hotels to add them to your bookmarks
            </p>
            <div className="mt-6">
              <Link
                to="/search"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Search Hotels
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Bookmarks; 