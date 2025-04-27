import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import HotelSearch from './pages/HotelSearch';
import Bookmarks from './pages/Bookmarks';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './components/PrivateRoute';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-100">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/search"
              element={
                <PrivateRoute>
                  <HotelSearch />
                </PrivateRoute>
              }
            />
            <Route
              path="/bookmarks"
              element={
                <PrivateRoute>
                  <Bookmarks />
                </PrivateRoute>
              }
            />
            <Route path="/" element={<Navigate to="/search" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App; 