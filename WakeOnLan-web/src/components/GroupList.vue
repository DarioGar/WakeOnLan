<template>
  <div>
    {{message}}
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
                  <v-select item-value return-object @input="assignRoom($event,group)" outlined dense solo class="mx-5" :items="rooms" item-text="name" label="Assign Room"></v-select>
                </v-col>

              </v-row>
            <v-list two-line>
              <template v-for="(member,n) in groupMembers">
                <v-list-item
                  :key="member"
                >
                  <v-list-item-avatar :color="roleColor(member.role)">
                  </v-list-item-avatar>

                  <v-list-item-content>
                    <v-list-item-title>Miembro: {{ member.name }}</v-list-item-title>
                  </v-list-item-content>
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
                    :v-model="group.name"
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
              @click="save"
            >
              Save
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
     </v-container>
  </div>
</template>


<script lang="ts">
import {Component,Vue} from "vue-property-decorator";
import GroupService from "../services/GroupService";
import RoomService from "../services/RoomService"
import { namespace } from "vuex-class";
const Auth = namespace("Auth");

@Component
export default class GroupList extends Vue {
  workGroups : any[] = []
  groupMembers : any[] = []
  rooms : any[] = []
  drawer = null
  dialog = false
  message = ""

  private group = {name:"",path:"",department:""}

    @Auth.State("user")
    private currentUser!: any;

    mounted() {
      this.getWorkGroup()
      this.getRooms()
    }

    roleColor(role : string){
      if (role == "admin" || role == "project_manager")
        return "blue"
      else
        return "grey darken-1"
    }

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
    getWorkGroup(){
      this.workGroups.length = 0
      this.groupMembers.length = 0
      GroupService.getWorkGroup(this.currentUser.username).then(
        (response) => {
          response.data.forEach((element : any) => {
            var work_group = {
              id : element[0],
              user_id : element[1],
              name : element[2],
              path : element[3],
              department : element[4],
              room : ""
            }
            this.getGroupMembers(element[0])
            this.workGroups.push(work_group)
          });
        },
        (error) => {
          this.message = "No groups yet assigned"
          }
      )
    }

    getGroupMembers(groupID : number){
      GroupService.getGroupMembers(groupID).then(
        (response) => {
          response.data.forEach((element : any) => {
            var member = {
              name : element[0],
              role : element[1],
              email : element[2]
            }
            this.groupMembers.push(member)
          });
        },
        (error) => {
          this.message =
            (error.response && error.response.data && error.response.data.message) ||
            error.message ||
            error.toString();
          }
      )
    }

    checkPermissions(){
      if (this.currentUser && this.currentUser.roles) {
        if((this.currentUser.roles.includes("admin")) || (this.currentUser.roles.includes("project_manager"))) {
          return true
        }
        else return false
      }
    }

    close () {
    this.dialog = false
    this.$nextTick(() => {
        this.group = {name:"",path:"",department:""}
    })
    }

    async save () {
    //Cambiar para que al guardar se inserte en la BBDD
    //REVISAR
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
    this.close()
    }
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
    }
    assignRoom(e,group){
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
    }

}
</script>