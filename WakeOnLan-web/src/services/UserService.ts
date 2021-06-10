import axios from 'axios';
import authHeader from './auth-header';

const API_URL = process.env.VUE_APP_AUTH_URL;

export interface Work_Group {
  ip : string;
  mac : string;
  cpu : string;
  ram : number;
  ssd : boolean;
  os : string;
  gpu : string;
  id : number
  reveal : boolean
  selectedPrograms : string[]
}

class UserService {
  sendInvite(sender: string,to: string, group: number) {
    return axios.post(API_URL + 'users/invite',{sender,to,group},{ headers: authHeader() });
  }
  getWorkGroup(username:any) {
    return axios.get(API_URL + 'users/'+username, { headers: authHeader() });
  }
  getUsers() {
    return axios.get(API_URL + 'users/user', { headers: authHeader() });
  }
  delUser(username:any,){
    return axios.delete(API_URL + 'users/'+username,{ headers: authHeader() });
  }
  updateUser(username: string, email: string, password: string,role: string,fullname: string) {
    return axios.put(API_URL + 'users/user',{username,email,password,role,fullname},{ headers: authHeader() });
  }
}

export default new UserService();