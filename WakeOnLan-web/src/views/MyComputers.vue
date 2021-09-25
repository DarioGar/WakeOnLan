<template>
  <v-row justify="center" class="mt-3">
    <v-col cols="8">
    <v-card elevation="10" class=" ma-5 pa-5" v-for="computer in computersOwned" :key="computer.mac">
      <v-row>
        <v-col cols="1">
          <v-icon :color="getColor(computer.online)">mdi-circle-slice-8</v-icon>
        </v-col>
        <v-col cols="5" md="5">
          <div class="text-uppercase">MAC : {{computer.mac}}</div>
          <div class="text-uppercase">IP : {{computer.ip}}</div>
        </v-col>
        <v-col cols="3">
          <span class="mt-3">Power Up Record</span>
        </v-col>
        <v-col align="end" cols="3">
          <v-btn class="mr-3" @click="selectedComputer(computer)">
            <v-icon color="blue-grey">mdi-pencil</v-icon>
          </v-btn>
        </v-col>
        <v-col cols="6">
          <v-card>
            <v-list
            height = "25vh"
            dense
            class="overflow-y-auto">
              <v-subheader>Users allowed to power up this computer</v-subheader>
              <v-list-item
              v-for="user in computer.usersAllowed"
              :key="user.username"
              >
                <v-list-item-content >
                  <span v-text="user.username"></span>
                </v-list-item-content>
                <v-list-item-content class = "pl-3">
                  <v-simple-checkbox
                  :ripple="false"
                  @click="changeAllowed(user,computer.mac)"
                  v-model="user.allowed"
                  ></v-simple-checkbox>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>
        <v-col cols="6" md="6">
          <v-data-table
          height = "25vh"
          hide-default-footer
          dense
          :items-per-page="-1"
          :headers="headers"
          :items="computer.powerLog"
          class="elevation-1"
        ></v-data-table>
        </v-col>
      </v-row>
    </v-card>
      <v-col cols="12">
        <ComputerDialog class="mx-5 mb-4" :edit="editComputer" :dialog="computerDialog" v-on:emit-dialog="dialog = false"/>
      </v-col>
  </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { namespace } from "vuex-class";
import ComputerService,{Computer} from "../services/ComputerService";
import ComputerDialog from '../components/ComputerDialog.vue'
import ProgramService from "../services/ProgramService"
const Auth = namespace("Auth");

@Component({components:{
      ComputerDialog
    },
    name : 'MyComputers'
})
// @vuese
// View that handles the personal computers of a user
export default class PC extends Vue {

  private computerDialog = false
  private editComputer = {}
  private message = ""
  private headers = [{text: "Username",align: "start",sortable: true, value: 'username'},
                     {text: "Time",align: "start",sortable: true, value: 'time'}]

  private computersOwned : Computer[] = []

  private users = []
  @Auth.State("user")
  private currentUser!: any;


  mounted() {
    if (!this.currentUser) {
      this.$router.push("/login");
    }
    this.getMyComputers()
  }

  getColor(online: boolean){
    if(online)
      return "green"
    else
      return "red"
  }

  selectedComputer(computer : any){
    this.editComputer = computer
    this.computerDialog = true
  }

  /**
   * @vuese
   * Used to change the permissions of a user to allowed or disallowed
   * @arg The first argument is a string representing the user who is to be changed
   * @arg The second argument is a boolean representing if the user is allowed(true) or not(false)
   * @arg The third argument is a string representing the mac of the computer that we want to allow access or not
   */
  changeAllowed(user : {username: string,allowed:boolean},mac : string){
    ComputerService.changeAllowance(user.username,user.allowed,mac).then(
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

  /**
   * @vuese
   * Used to get the personal computers of the current user
 */
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
            name : element[8],
            online : element[9],
            selectedPrograms : [],
            usersAllowed : []
          }
          this.getPrograms(computer)
          this.getUsersAllowed(computer)
          this.getPowerLog(computer)
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

  /**
   * @vuese
   * Used to get the programs available for the computer
   * @arg The argument is a string representing the computer mac
 */
  getPrograms(computer : any){
    ProgramService.getPrograms(computer.mac).then(
      (response) => {
        response.data.forEach((element: any) => {
          computer.selectedPrograms.push(element[2])
        });
      },
      (error) => {
        this.message =
          (error.response && error.response.data && error.response.data.message) ||
          error.message ||
          error.toString();
      }
    );
  }

  /**
   * @vuese
   * Used to get the bootup log of a computer with username and time
   * @arg The argument is a string representing the computer mac
 */
  getPowerLog(computer:any){
    var log : {username: string,time:string}[] = []
    ComputerService.getLogsFor(computer.mac).then(
      (response) => {
        response.data.forEach((element: any) => {
          var data = {
            username: element[0],
            time : element[1]
          }
          log.push(data)
        });
        computer.powerLog=log
      },
      (error) => {
        this.message =
            (error.response && error.response.data && error.response.data.message) ||
            error.message ||
            error.toString(); 
      }
    )
  }
  
  /**
   * @vuese
   * Used to get users allowed to power up the computer
   * @arg The argument is a string representing the computer mac
 */
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
        computer.usersAllowed = allowed
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