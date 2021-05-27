import axios from 'axios';
import authHeader from './auth-header';

const API_URL = process.env.VUE_APP_AUTH_URL;

class ComputerService {
  getAllComputers() {
    return axios.get(API_URL + 'macs/mac', { headers: authHeader() });
  }
  getComputer(mac : any) {
    return axios.get(API_URL + 'macs/mac/' + mac, { headers: authHeader() });
  }
  getComputerForUser(username : any) {
    return axios.get(API_URL + 'macs/mac/' + username, { headers: authHeader() });
  }
}

export default new ComputerService();