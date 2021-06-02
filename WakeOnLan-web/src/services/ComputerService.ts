import axios from 'axios';
import authHeader from './auth-header';

const API_URL = process.env.VUE_APP_AUTH_URL;

export interface Computer {
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

class ComputerService {
  getAvailableComputersForUser(username : any) {
    return axios.get(API_URL + 'macs/' + username, { headers: authHeader() });
  }
  schedulePowerOn(computerId : number,username : string, days : string[],time : string){
    return axios.post(API_URL + 'schedule',{computerId,username,days,time},{ headers: authHeader() })
  }
  tryToPowerComputerOn(mac : string,username : string){
    return axios.post(API_URL + 'macs/mac',{username,mac},{ headers: authHeader() })
  }
}

export default new ComputerService();