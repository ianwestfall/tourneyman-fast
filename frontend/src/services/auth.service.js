import axios from 'axios';
import User from '../models/user';

const API_URL = process.env.VUE_APP_API_URL;

class AuthService {
  static async login(user) {
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
      localStorage.setItem('user', JSON.stringify(safeUser));
      localStorage.setItem('userToken', JSON.stringify(response.data));
    }

    return response.data;
  }

  static logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('userToken');
  }

  static register(user) {
    const endpoint = '/auth/users';
    return axios.post(API_URL + endpoint, {
      email: user.email,
      password: user.password,
    });
  }
}

export default AuthService;
