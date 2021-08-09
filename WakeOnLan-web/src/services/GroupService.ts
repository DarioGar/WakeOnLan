import axios from 'axios';
import authHeader from './auth-header';

const API_URL = process.env.VUE_APP_AUTH_URL;

class GroupService {
  insertGroup(groupLeader: string, name: string, path: string, department: string) {
    return axios.post(API_URL + 'groups',{groupLeader,name,path,department}, { headers: authHeader() });
  }
  getGroupMembers(groupID: number) {
    return axios.get(API_URL + 'groups/members/'+groupID, { headers: authHeader() });
  }
  accept(id: number, groupId: number, userId: number) {
    return axios.put(API_URL + 'users/invites/accept',{id,groupId,userId},{ headers: authHeader() })
  }
  deny(id: number) {
    return axios.put(API_URL + 'users/invites/deny',{id},{ headers: authHeader() })
  }
  getInvitationsFor(username: string) {
    return axios.get(API_URL + 'users/invites/' + username,{ headers: authHeader() });
  }
  sendInvite(sender: string,to: string, group: number) {
    return axios.post(API_URL + 'users/invites/',{sender,to,group},{ headers: authHeader() });
  }
  getWorkGroup(username:string) {
    return axios.get(API_URL + 'groups/'+username, { headers: authHeader() });
  }
  delGroup(groupID : number){
    return axios.delete(API_URL + 'groups/' + groupID, { headers: authHeader() });
  }
  assignRoom(roomID : number,groupID : number){
    return axios.post(API_URL + 'groups/room',{roomID,groupID},{ headers: authHeader() });
  }
  deassignRoom(groupID : number){
    return axios.put(API_URL + 'groups/room/'+ groupID, { headers: authHeader() });
  }
  getRoom(groupID : number){
    return axios.get(API_URL + 'groups/room/'+ groupID, { headers: authHeader() });
  }
  removeUserFromGroup(username : string,groupID : number){
    return axios.delete(API_URL + 'groups/members/'+groupID + "/" + username, { headers: authHeader() });
  }

}

export default new GroupService();