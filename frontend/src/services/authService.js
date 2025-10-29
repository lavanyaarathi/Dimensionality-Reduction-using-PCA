/**
 * Authentication service for PCA project.
 * Handles user login, registration, and token management.
 */
console.log("Backend API:", process.env.REACT_APP_API_URL);
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class AuthService {
  async login(username, password) {
    try {
      console.log(`Attempting login to: ${API_BASE_URL}/api/login`);
      
      const response = await fetch(`${API_BASE_URL}/api/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('username', data.username);
        console.log('Login successful');
        return { success: true, data };
      } else {
        console.error('Login failed:', data.message);
        return { success: false, message: data.message };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, message: 'Network error. Please check your connection and try again.' };
    }
  }

  async register(username, email, password) {
    try {
      console.log(`Attempting registration to: ${API_BASE_URL}/api/register`);
      
      const response = await fetch(`${API_BASE_URL}/api/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        console.log('Registration successful');
        return { success: true, data };
      } else {
        console.error('Registration failed:', data.message);
        return { success: false, message: data.message };
      }
    } catch (error) {
      console.error('Register error:', error);
      return { success: false, message: 'Network error. Please check your connection and try again.' };
    }
  }

  async logout() {
    const token = this.getToken();
    
    try {
      console.log('Logging out...');
      await fetch(`${API_BASE_URL}/api/logout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      console.log('Logout complete');
    }
  }

  async verifyToken() {
    const token = this.getToken();
    
    if (!token) {
      console.log('No token found');
      return false;
    }

    try {
      console.log('Verifying token...');
      const response = await fetch(`${API_BASE_URL}/api/verify`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const isValid = response.ok;
      console.log('Token valid:', isValid);
      return isValid;
    } catch (error) {
      console.error('Token verification error:', error);
      return false;
    }
  }

  getToken() {
    return localStorage.getItem('token');
  }

  getUsername() {
    return localStorage.getItem('username');
  }

  isAuthenticated() {
    return !!this.getToken();
  }
}

const authService = new AuthService();
export default authService;

