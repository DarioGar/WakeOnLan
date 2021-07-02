import axios from 'axios';
import authHeader from './auth-header';

const API_URL = process.env.VUE_APP_AUTH_URL;

class UserService {
  getUsers() {
    return axios.get(API_URL + 'users/user', { headers: authHeader() });
  }
  delUser(username:any,){
    return axios.delete(API_URL + 'users/user/'+username,{ headers: authHeader() });
  }
  updateUserData(username: string, email: string, password: string,role: string,fullname: string,pw : boolean) {
    return axios.put(API_URL + 'users/user',{username,email,password,role,fullname,pw},{ headers: authHeader() });
  }
}

export default new UserService();