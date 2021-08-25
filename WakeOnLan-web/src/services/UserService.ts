import axios from 'axios';
import authHeader from './auth-header';

const API_URL = process.env.VUE_APP_AUTH_URL;

export interface User {
  id : number;
  username : string;
  email : string;
  role : string;
  password : string;
  fullname : string;
}

class UserService {
  getUsers() {
    return axios.get(API_URL + 'users/user/new', { headers: authHeader() });
  }
  delUser(username:string){
    return axios.delete(API_URL + 'users/user/'+username,{ headers: authHeader() });
  }
  updateUserData(username: string, email: string, password: string,role: string,fullname: string,pw : boolean) {
    return axios.put(API_URL + 'users/user/update',{username,email,password,role,fullname,pw},{ headers: authHeader() });
  }
  
}

export default new UserService();