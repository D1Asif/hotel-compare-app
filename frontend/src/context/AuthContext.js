import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext(null);

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await fetch('http://localhost:8000/verify-token', {
            headers: { Authorization: `Bearer ${token}` }
          });
          if (!response.ok) {
            throw new Error('Token verification failed');
          }
          const data = await response.json();
          setUser(data);
        } catch (error) {
          console.error('Auth verification error:', error);
          localStorage.removeItem('token');
          setUser(null);
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (email, password) => {
    try {
      const response = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Login failed');
      }

      const data = await response.json();
      console.log('Login response:', data);
      
      const { access_token, refresh_token, token_type } = data;
      
      localStorage.setItem('token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      
      const userState = { email };
      setUser(userState);
      
      console.log('Stored token:', access_token);
      
      return { success: true, user: userState };
    } catch (error) {
      console.error('Login error:', error);
      return {
        success: false,
        error: error.message || 'Login failed'
      };
    }
  };

  const register = async (email, username, password) => {
    try {
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, username, password })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Registration failed');
      }

      const data = await response.json();
      console.log('Register response:', data);
      
      const { access_token, refresh_token, token_type } = data;
      
      localStorage.setItem('token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      
      const userState = { email, username };
      setUser(userState);
      
      console.log('Stored token:', access_token);
      
      return { success: true, user: userState };
    } catch (error) {
      console.error('Registration error:', error);
      return {
        success: false,
        error: error.message || 'Registration failed'
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}; 