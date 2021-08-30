<template>
  <div>
    <v-container>
      <v-row>
        <v-col
          v-for="group in workGroups"
          :key="group"
          cols="12"
        >
          <v-card>
            <v-card-title
              class="text-h5"
              v-text="group.name"
            ></v-card-title>
              <v-row>
                <v-col class="mx-3" cols="5">
                  <strong>Departamento: </strong> {{ group.department }}
                  <strong class="ml-2">Ubicación: </strong> {{ group.path }}
                </v-col>
                <v-col align="center" cols="6">
                  <v-btn
                  color="error"
                  @click="deleteGroup(group)"
                >
                  Delete Group
                </v-btn>
                </v-col>
                <v-col md="3" cols="6">
                  <v-select :disabled="group.room" item-value return-object @input="assignRoom($event,group)" outlined dense solo class="mx-5" :items="rooms" item-text="name" label="Assign Room"></v-select>
                </v-col>
                <v-col align="start" md="9" cols="6">
                    <div>
                      <v-menu
                        open-on-hover
                        offset-y
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn
                            :disabled="!group.room"
                            v-bind="attrs"
                            v-on="on"
                          >
                            Assigned Room : {{group.room}}
                          </v-btn>
                        </template>
                            <v-btn @click="deassignRoom(group)">Click to stop using the room</v-btn>
                      </v-menu>
                    </div>
                </v-col>
              </v-row>
            <v-list two-line>
              <template v-for="(member,n) in group.members">
                <v-list-item
                  :key="member"
                  
                >
                  <v-list-item-avatar :color="roleColor(member.role)">
                  </v-list-item-avatar>

                  <v-list-item-content>
                    <v-list-item-title>Miembro: {{ member.name }}</v-list-item-title>
                    
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-btn @click="removeUserFromGroup(member.name,group,n)">Remove user</v-btn>
                  </v-list-item-action>
                </v-list-item>

                <v-divider
                  v-if="n !== 6"
                  :key="`divider-${n}`"
                  inset
                ></v-divider>
              </template>
            </v-list>
          </v-card>
        </v-col>
      </v-row>
      
      <v-dialog
        v-model="dialog"
        max-width="500px"
      >
        <template v-if="checkPermissions()" v-slot:activator="{ on, attrs }">
          <v-btn
            color="primary"
            dark
            class="ma-5"
            v-bind="attrs"
            v-on="on"
          >
            New Group
          </v-btn>
        </template>
        <v-card>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col
                  cols="12"
                  sm="6"
                  md="6"
                >
                  <v-text-field
                    label="Name*"
                    required
                    v-model="group.name"
                  ></v-text-field>
                </v-col>
                <v-col 
                cols="12"
                sm="6"
                md="6">
                  <v-text-field
                    label="Address*"
                    required
                    v-model="group.path"
                  ></v-text-field>
                </v-col>
                <v-col
                  cols="12"
                  sm="6"
                  md="4"
                >
                  <v-text-field
                    label="Department*"
                    required
                    v-model="group.department"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="blue darken-1"
              text
              @click="close"
            >
              Cancel
            </v-btn>
            <v-btn
              color="blue darken-1"
              text
              @click="saveGroup"
            >
              Save
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
     </v-container>
     {{message2}}
  </div>
</template>


<script lang="ts">
import {Component,Vue} from "vue-property-decorator";
import GroupService from "../services/GroupService";
import RoomService from "../services/RoomService"
import { namespace } from "vuex-class";
const Auth = namespace("Auth");

@Component({
  name: 'GroupList'
})
// @vuese
export default class GroupList extends Vue {

  private workGroups : any[] = []
  private rooms : any[] = []
  private drawer = null
  private dialog = false
  private message = ""
  private message2= ""

  private group = {name:"",path:"",department:""}

    @Auth.State("user")
    private currentUser!: any;
  /**
   * @vuese
   * Used to initialize data
   */
    mounted() {
      this.getWorkGroup()
      this.getRooms()
    }

  /**
   * @vuese
   * Used to get the user color based on their role
   * @arg The argument is a string value representing the user role
   */
    roleColor(role : string){
      if (role == "admin" || role == "project_manager")
        return "blue"
      else
        return "grey darken-1"
    }
  /**
   * @vuese
   * Used to get the rooms, retrieves all rooms and shows only the ones that are not occupied
   */
    getRooms(){
      RoomService.getRooms().then(
        (response) => {
          response.data.forEach((element : any) => {
            var room = {
              id : element[0],
              name : element[2],
            }
            if(!element[1])
              this.rooms.push(room)
          });
        },
        (error) => {
          this.message = "No groups yet assigned"
          }
      )
    }
  /**
   * @vuese
   * Used to get the user's work groups if any, their members and room assigned
   */
    getWorkGroup(){
      this.workGroups.length = 0
      GroupService.getWorkGroup(this.currentUser.username).then(
        (response) => {
          response.data.forEach((element : any) => {
            var work_group = {
              id : element[0],
              user_id : element[1],
              name : element[2],
              path : element[3],
              department : element[4],
              room : "",
              members : []
            }
            work_group.members = this.getGroupMembers(element[0])
            this.roomAssigned(work_group)
            this.workGroups.push(work_group)
          });
        },
        (error) => {
          this.message = "No groups yet assigned"
          }
      )
    }
  /**
   * @vuese
   * Used to get the members of a given group
   * @arg The argument is a number indicating the ID of the group
   */
    getGroupMembers(groupID : number){
      var groupMembers : any[] = []
      GroupService.getGroupMembers(groupID).then(
        (response) => {
          response.data.forEach((element : any) => {
            var member = {
              name : element[0],
              role : element[1],
              email : element[2]
            }
            groupMembers.push(member)
          });
        },
        (error) => {
          this.message =
            (error.response && error.response.data && error.response.data.message) ||
            error.message ||
            error.toString();
          }
      )
      return groupMembers
    }

  /**
   * @vuese
   * Used to get the room assigned to a given group
   * @arg The argument is a number presesenting the group ID
   */
    roomAssigned(work_group : any){
      var location = ""
      GroupService.getRoom(work_group.id).then(
        (response) => {
            work_group.room = response.data
        },
        (error) => {
          this.message =
            (error.response && error.response.data && error.response.data.message) ||
            error.message ||
            error.toString();
            work_group.room = null
          }
      )
    }

  /**
   * @vuese
   * Used to check for the roles of the current user
   */
    checkPermissions(){
      if (this.currentUser && this.currentUser.roles) {
        if((this.currentUser.roles.includes("admin")) || (this.currentUser.roles.includes("project_manager"))) {
          return true
        }
        else return false
      }
    }

  /**
   * @vuese
   * Used to close the "New group" dialog
   */
    close () {
    this.dialog = false
    this.$nextTick(() => {
        this.group = {name:"",path:"",department:""}
    })
    }

  /**
   * @vuese
   * Used to save the newly created making a call to the API
   */
    async saveGroup () {
      GroupService.insertGroup(this.currentUser.username,this.group.name,this.group.path,this.group.department).then(
        (response) => {
          this.message = response.data
        },
        (error) => {
          this.message =
            (error.response && error.response.data && error.response.data.message) ||
            error.message ||
            error.toString();
          }
      )
      window.location.reload()
    this.close()
    }
    
  /**
   * @vuese
   * Used to delete a given group
   * @arg The argument is a group
   */
    deleteGroup(group : any){
      GroupService.delGroup(group.id).then(
        (response) => {
          this.message = response.data
        },
        (error) => {
          this.message =
            (error.response && error.response.data && error.response.data.message) ||
            error.message ||
            error.toString();
          }
      )
      window.location.reload()
    }

  /**
   * @vuese
   * Used to assign a room to a group
   * @arg The first argument is a room value representing the room that has to be assigned
   * @arg The second argument is a group value representing the group
   */
    assignRoom(e : any,group : any){
      GroupService.assignRoom(e.id,group.id).then(
        (response) => {
          this.message = response.data
        },
        (error) => {
          this.message =
            (error.response && error.response.data && error.response.data.message) ||
            error.message ||
            error.toString();
          }
      )
      window.location.reload()
    }
  /**
   * @vuese
   * Used to deassign a room from a given group
   * @arg The argument is a group
   */
    deassignRoom(group: any){
      group.room = null
      GroupService.deassignRoom(group.id).then(
        (response) => {
          this.message = response.data
        },
        (error) => {
          this.message =
            (error.response && error.response.data && error.response.data.message) ||
            error.message ||
            error.toString();
          }
      )
      window.location.reload()
    }
  /**
   * @vuese
   * Used to remove a user from some group
   * @arg The first argument is the user's username
   * @arg The second argument is a group
   * @arg The third argument is the index of that user in the group members list
   */
    removeUserFromGroup(username: string,group:any,n : number){
      group.members.splice(n,1)
      GroupService.removeUserFromGroup(username,group.id).then(
        (response) => {
          this.message = response.data
        },
        (error) => {
          this.message =
            (error.response && error.response.data && error.response.data.message) ||
            error.message ||
            error.toString();
          }
      )
    }
}
</script>