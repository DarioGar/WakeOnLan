<template>
  <v-row justify="center">
    <v-col cols="10">
    <span>{{message}}</span>
    <v-card elevation="10" class=" ma-5 pa-5" v-for="computer in computersOwned" :key="computer.mac">
      <v-row>
        <v-col cols="1">
          <v-icon :color="`${computer.online}`">mdi-circle-slice-8</v-icon>
        </v-col>
        <v-col cols="5" md="5">
          <div class="text-uppercase">MAC : {{computer.mac}}</div>
          <div class="text-uppercase">IP : {{computer.ip}}</div>
          <v-list
          v-for="user in getUsersAllowed(computer)"
          :key="user.username"
          dense
          style="max-height: 200px"
          class="overflow-y-auto">
            <v-subheader>Users allowed to power up this computer</v-subheader>
            <v-list-item
            >
              <v-list-item-content>
                <span v-text="user.username"></span>
              </v-list-item-content>
              <v-list-item-content>
                <v-simple-checkbox
                v-model="user.allowed"
                ></v-simple-checkbox>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-col>
        <v-col cols="6" md="6">
          <v-data-table
          height = "25vh"
          dense
          :headers="headers"
          :items="getPowerLog(computer)"
          class="elevation-1"
        ></v-data-table>
        </v-col>
      </v-row>
      <v-icon @click="showDetails(computer)">mdi-help-circle</v-icon>
    </v-card>
  </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { namespace } from "vuex-class";
import ComputerService,{Computer} from "../services/ComputerService";
const Auth = namespace("Auth");

@Component
export default class PC extends Vue {

  private message = ""
  private headers = [{text: "Username",align: "start",sortable: true, value: 'username'},
                     {text: "Time",align: "start",sortable: true, value: 'time'}]
  //Variable to store the users who have powered each pc and when
  private log = [{}]
  private computersOwned : Computer[] = []

  @Auth.State("user")
  private currentUser!: any;


  mounted() {
    if (!this.currentUser) {
      this.$router.push("/login");
    }
    this.getMyComputers()
  }

  getMyComputers(){
    this.computersOwned.length = 0
    ComputerService.getMyComputers(this.currentUser.username).then(
      (response) => {
        response.data.forEach((element: any) => {
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
            online : false,
            selectedPrograms : []
          }
          this.computersOwned.push(computer)
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

  showDetails(computer : any){
    this.message = computer
  }

  getPowerLog(computer:any){
    this.log.length = 0
    ComputerService.getLogsFor(computer.mac).then(
      (response) => {
        response.data.forEach((element: any) => {
          var log = {
            username: element[0],
            time : element[1]
          }
          this.log.push(log)
        });
        return this.log
      },
      (error) => {
        this.message =
            (error.response && error.response.data && error.response.data.message) ||
            error.message ||
            error.toString(); 
      }
    )
  }
  
  getUsersAllowed(computer : any){
    var allowed : {username: string,allowed:boolean}[] = []
    allowed.length = 0
    ComputerService.getUsersAllowedOn(computer.mac).then(
      (response) => {
        response.data.forEach((element: any) => {
          var user = {
            username: element[0],
            allowed: element[1]
          }
          allowed.push(user)
        });
        return allowed
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