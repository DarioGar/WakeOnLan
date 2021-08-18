import axios from 'axios';
import authHeader from './auth-header';

const API_URL = process.env.VUE_APP_AUTH_URL;

export interface Computer {
  ip : string;
  name : string;
  mac : string;
  cpu : string;
  ram : number;
  ssd : boolean;
  os : string;
  gpu : string;
  id : number;
  reveal : boolean;
  online : boolean;
  selectedPrograms : string[];
  usersAllowed : {username:string,allowed:boolean}[];
  
}

class ComputerService {
  getAvailableComputersForUser(username : any) {
    return axios.get(API_URL + 'macs/for/' + username, { headers: authHeader() });
  }

  getUsersAllowedOn(mac : string){
    return axios.get(API_URL + 'macs/allowed/' + mac,{ headers: authHeader() });
  }

  getLogsFor(mac : string){
    return axios.get(API_URL + 'macs/log/' + mac,{ headers: authHeader() });
  }

  getMyComputers(username : any){
    return axios.get(API_URL + 'macs/mac/' + username,{headers: authHeader()});
  }

  registerNew(mac : string,ip : string,ram : number,cpu : string,gpu : string,os : string,ssd : boolean,owner : string,name: string){
    return axios.post(API_URL + 'macs/new',{
      mac,
      ip,
      ram,
      cpu,
      gpu,
      os,
      ssd
      ,owner
      ,name
    },{headers: authHeader()});
  }
  
  update(mac : string,ip : string,ram : number,cpu : string,gpu : string,os : string,ssd : boolean,name: string){
    return axios.put(API_URL + 'macs/update',{
      mac,
      ip,
      ram,
      cpu,
      gpu,
      os,
      ssd,
      name
    },{headers: authHeader()});
  }

  delete(mac: string){
    return axios.delete(API_URL + 'macs/' + mac,{headers: authHeader()});
  }
  
  schedulePowerOn(computerId : number,username : string, days : string[],time : string){
    return axios.post(API_URL + 'schedule',{
      computerId,
      username,
      days,
      time
    },{ headers: authHeader() })
  }

  tryToPowerComputerOn(mac : string,username : string){
    return axios.post(API_URL + 'macs/power',{username,mac},{ headers: authHeader() })
  }

  changeAllowance(username : string,allowed : boolean,mac : string){
    return axios.post(API_URL + 'macs/allowed/' + mac,{username,allowed},{ headers: authHeader() })
  }
  getDaysData(){
    return axios.get(API_URL + 'macs/days/',{ headers: authHeader() })
  }
  getOnline(){
    return axios.get(API_URL + 'macs/online/',{ headers: authHeader() })
  }
  getActiveData(){
    return axios.get(API_URL + 'macs/users/',{ headers: authHeader() })
  }
}

export default new ComputerService();