import axios from 'axios';
import authHeader from './auth-header';

const API_URL = process.env.VUE_APP_AUTH_URL;

export interface Room {
    id : number,
    location : string,
    capacity: number,
    use : string,
    computers : {ip : string}[]


}

class RoomService {

    getRooms(){
      return axios.get(API_URL + 'rooms/room/',{ headers: authHeader() });
      }
    getComputersInRoom(roomID : number){
      return axios.get(API_URL + 'rooms/room/' + roomID,{ headers: authHeader() });
    }
    newRoom(location: string,capacity : number,use: string){
      return axios.post(API_URL +'rooms/room/',{location,capacity,use},{ headers: authHeader() });
    }
    delRoom(roomID : number){
      return axios.delete(API_URL + 'rooms/room/' + roomID,{ headers: authHeader() });
    }
    getComputersWithoutRoom(){
      return axios.get(API_URL +'rooms/room/unassigned/',{ headers: authHeader() });
    }
    SetComputers(roomID : number,computers : []){
      return axios.put(API_URL +'rooms/room/unassigned/',{roomID,computers},{ headers: authHeader() });
    }

}

export default new RoomService();