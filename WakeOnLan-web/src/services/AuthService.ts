import axios from 'axios';
import authHeader from './auth-header';
const API_URL = process.env.VUE_APP_AUTH_URL;


class AuthService {
  login(username: string, password: string) {
    return axios
      .post(API_URL + 'users/login', {
        username,
        password
      })
      .then(response => {
        if (response.data.accessToken) {
          localStorage.setItem('user', JSON.stringify(response.data));
        }

        return response.data;
      });
  }

  logout() {
    localStorage.removeItem('user');
  }

  register(username: string, email: string, password: string,role: string,fullname: string) {
    return axios.post(API_URL + 'users/signup', {
      username,
      email,
      password,
      role,
      fullname
    },{ headers: authHeader() });
  }
}

export default new AuthService();