import axios from 'axios';
import authHeader from './auth-header';

const API_URL = process.env.VUE_APP_API_URL;

class UserService {
  static async getProfile() {
    const endpoint = '/users/me';

    const response = await axios.get(API_URL + endpoint, { headers: authHeader() });
    return response.data;
  }
}

export default UserService;
