<template>
  <v-row justify="center" class="mt-3">
    <v-col cols="8">
      <v-row>
        <v-col
          v-for="room in rooms"
          :key="room.id"
          cols="12"
        >
          <v-card>
            <v-card-title
              class="text-h5"
              v-text="room.location"
            ></v-card-title>
              <v-row align="start">
                <v-col class="mx-3" cols="5">
                  <strong>Capacity: </strong> {{ room.capacity }}
                  <strong class="ml-2">Expected use: </strong> {{ room.use }}
                </v-col>
                <v-col align="center" cols="6">
                  <v-btn
                  color="error"
                  @click="deleteRoom(room)"
                >
                  Delete Room
                </v-btn>
                </v-col>
              </v-row>
              <v-row class = "mx-3" align="center">
                <v-col cols="5">
                  <v-select
                  v-model="room.computersToRemove"
                  :items="room.computers"
                  item-value
                  return-object
                  item-text="name"
                  label="Computers in room"
                  @change="event($event,room)"
                  multiple
                >
                </v-select>
                </v-col>
                <v-col align="center">
                  <div>Select to swap between</div>
                  <v-btn class="mt-2" @click="swap(room)">
                    <v-icon>
                      mdi-swap-horizontal
                    </v-icon>
                  </v-btn>

                </v-col>
                <v-col cols="5">
                  <v-select
                  v-model="room.computersToAssign"
                  :items="computersAvailable"
                  item-value
                  return-object
                  item-text="name"
                  label="Computers not assigned to any room"
                  multiple
                >
                </v-select>
                </v-col>
              </v-row>
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
            New Room
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
                    label="Location*"
                    v-model="room.location"
                    required
                  ></v-text-field>
                </v-col>
                <v-col 
                cols="12"
                sm="6"
                md="6">
                  <v-text-field
                    label="Capacity*"
                    v-model="room.capacity"
                    required
                  ></v-text-field>
                </v-col>
                <v-col
                  cols="12"
                  sm="6"
                  md="4"
                >
                  <v-select
                    label="Use*"
                    required
                    v-model="room.use"
                    :items="['iot', 'datascience', 'cybersecurity', 'regular']"
                  ></v-select>
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
              @click="saveRoom"
            >
              Save
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      </v-col>
    </v-row>
</template>

<script lang = "ts">
import { Component, Vue } from "vue-property-decorator";
import { namespace } from "vuex-class";
import RoomService,{Room} from "../services/RoomService"
import {Computer} from "../services/ComputerService"
const Auth = namespace("Auth");

@Component
export default class Rooms extends Vue {

    private rooms : Room[] = []
    private message = {}
    private dialog = false
    private computersAvailable = [{}]
    private room = {location : "",capacity : 0,use : ""}

    @Auth.State("user")
    private currentUser!: any;

    mounted() {
      this.computersAvailable.pop()
      this.getRooms()
      this.getComputersWithoutRoom()
    }
    
    event(e : any,room : any){
      room.computersToRemove = e
    }

    swap(room : any){
      room.computersToAssign.forEach((computer : any,index : any) => {
        room.computers.push(computer)
      })
      this.computersAvailable = this.computersAvailable.filter(x => !room.computersToAssign.includes(x))
      room.computersToRemove.forEach((computer : any,index : any) => {
        this.computersAvailable.push(computer)
      })
      room.computers = room.computers.filter((x : any) => !room.computersToRemove.includes(x))
      room.computersToAssign = []
      room.computersToRemove = []
      
      RoomService.SetComputers(room.id,room.computers).then(
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

    checkPermissions(){
      if (this.currentUser && this.currentUser.roles) {
        if((this.currentUser.roles.includes("admin")) || (this.currentUser.roles.includes("project_manager"))) {
          return true
        }
        else return false
      }
    }

    getRooms(){
      this.rooms.length = 0
        RoomService.getRooms().then(
        (response) => {
          response.data.forEach((element : any) => {
            var room = {
                  id : element[0],
                  location : element[2],
                  capacity : element[3],
                  use : element[4],
                  computers : [],
                  computersToAssign : [],
                  computersToRemove : []
            }
            this.getComputersInRoom(room)
            this.rooms.push(room)
          });
          this.message = this.rooms
        },
        (error) => {
          this.message =
            (error.response && error.response.data && error.response.data.message) ||
            error.message ||
            error.toString();
          }
      )
    }

    getComputersInRoom(room : Room){
      RoomService.getComputersInRoom(room.id).then(
        (response) => {
          response.data.forEach((element : any) => {
            var computer : Computer = {
                        ip : element[0],
                        mac : element[1],
                        cpu : element[2],
                        ram : element[3],
                        ssd : element[4],
                        os : element[5],
                        gpu : element[6],
                        id : element[7],
                        reveal : false,
                        name : element[8],
                        online : element[9],
                        selectedPrograms : [],
                        usersAllowed : []
                      }
            room.computers.push(computer)
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

    getComputersWithoutRoom(){
      RoomService.getComputersWithoutRoom().then(
        (response) => {
          response.data.forEach((element : any) => {
            var computer : Computer = {
                        ip : element[0],
                        mac : element[1],
                        cpu : element[2],
                        ram : element[3],
                        ssd : element[4],
                        os : element[5],
                        gpu : element[6],
                        id : element[7],
                        reveal : false,
                        name : element[8],
                        online : element[9],
                        selectedPrograms : [],
                        usersAllowed : []
                      }
            this.computersAvailable.push(computer)
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

    saveRoom(){
      RoomService.newRoom(this.room.location,this.room.capacity,this.room.use).then(
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
      this.dialog = false
    }

    close(){
      this.dialog = false
    }

    deleteRoom(room : any){
      RoomService.delRoom(room.id).then(
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
}
</script>