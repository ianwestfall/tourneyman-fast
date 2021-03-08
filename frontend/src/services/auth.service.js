import axios from 'axios';
import User from '../models/user';

const API_URL = process.env.VUE_APP_API_URL;

class AuthService {
  static async login(user) {
    if (!user) {
      throw new TypeError('user must not be null/undefined');
    } else if (!user.email || !user.password) {
      throw new TypeError('user must have an email and a password');
    }

    const endpoint = '/auth/token';
    const data = new FormData();
    data.append('username', user.email);
    data.append('password', user.password);

    const response = await axios.post(API_URL + endpoint, data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (response.data.access_token) {
      const safeUser = new User(user.email);
      window.localStorage.setItem('user', JSON.stringify(safeUser));
      window.localStorage.setItem('userToken', JSON.stringify(response.data));
    }

    return response.data;
  }

  static logout() {
    window.localStorage.removeItem('user');
    window.localStorage.removeItem('userToken');
  }

  static async register(user) {
    if (!user) {
      throw new TypeError('user must not be null/undefined');
    } else if (!user.email || !user.password) {
      throw new TypeError('user must have an email and a password');
    }

    const endpoint = '/auth/users';
    return axios.post(API_URL + endpoint, {
      email: user.email,
      password: user.password,
    });
  }
}

export default AuthService;
