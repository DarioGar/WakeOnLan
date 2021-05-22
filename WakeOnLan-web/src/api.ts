import axios from 'axios';

const authService = axios.create({
  baseURL: process.env.VUE_APP_AUTH_URL,
  withCredentials: true,
  xsrfCookieName: 'csrf_access_token'
});
export { authService };

