import axios from 'axios';
import authHeader from './auth-header';

const API_URL = process.env.VUE_APP_AUTH_URL;

export interface Program {
    name : string,
    path : string
}

class Programs {

    getPrograms(mac : string){
        return axios.get(API_URL + 'macs/programs/' + mac,{ headers: authHeader() });
    }

    updatePrograms(programs : {name: string,path : string}[],computer: string){
        return axios.post(API_URL + 'macs/programs/new',{programs,computer},{ headers: authHeader() });
    }

    addProgramForNextPowerUp(programs : string[],computer : string){
        return axios.post(API_URL + 'macs/programs/launch/' + computer,{programs,computer},{ headers: authHeader() })
    }

}

export default new Programs();