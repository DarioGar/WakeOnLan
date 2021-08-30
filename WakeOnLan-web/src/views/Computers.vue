<template>
  <v-row justify="center" class="mt-3">
    <v-col cols="8">
      <span>
        Select programs to launch, time and days to power up the computer and hit the power button or, alternatively just hit the power button to turn the computer on now
      </span>
      <span class="red--text">{{message}}</span>
      <v-row class="my-5">
        <v-col cols="12">
          <ComputerDialog class="mx-1" :dialog="computerDialog"/>
        </v-col>
        <v-col class="my-2"
          v-for="(computer,i) in computers"
          :key="i"
          cols="4" sm="4" md="3" xl=3
        >
          <v-card >
            <v-row>
              <v-col cols="1" sm="2" md="2" xl="3">
                <v-icon :class="size()">mdi-desktop-classic</v-icon>
              </v-col>
              <v-col>
                <v-card-title class="text-capitalize ml-4">{{computer.os}}</v-card-title>
                <v-card-text>{{computer.name}}</v-card-text>
              </v-col>
            </v-row>
            <v-card-actions class="mx-1">
              <v-btn class="mr-1" @click="computer.reveal = !computer.reveal ">
                More
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn class="ml-1" @click="powerComputer(computer)">
                <v-icon :color="getColor(computer.online)">
                  mdi-power
                </v-icon>
              </v-btn>
            </v-card-actions>
                <v-expand-transition>
                  <v-card
                    v-if="computer.reveal"
                    class="transition-fast-in-fast-out v-card--reveal"
                    style="height: 100%;"
                  >
                  <ProgramPicker v-bind ='{computer : computer}' v-on:emit-programs="savePrograms"/>
                  <PowerOnComponent v-bind ='{computer : computer}' v-on:emit-time="saveTime"/>
                  </v-card>
                </v-expand-transition>
          </v-card>
        </v-col>
      </v-row> 
    </v-col>
  </v-row>   
</template>

<script lang = "ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import { namespace } from "vuex-class";
import vuetify from "vuetify"
import ComputerService,{Computer} from "../services/ComputerService";
import ProgramService from "../services/ProgramService";
const Auth = namespace("Auth");
import ProgramPicker from '../components/ProgramPicker.vue'
import PowerOnComponent from '../components/PowerOnComponent.vue'
import ComputerDialog from '../components/ComputerDialog.vue'


@Component({components:{
      ProgramPicker,
      PowerOnComponent,
      ComputerDialog
    },
    name : 'Computers'
})
// @vuese
  export default class Computers extends Vue{
    private computers : Computer[] = []
    private message = ""
    private timeMap = new Map()
    private computerDialog = false

    @Auth.Getter
    private isLoggedIn!: boolean;

    @Auth.State("user")
    private currentUser!: any;

  /**
   * @vuese
   * Used to control the size of the icons to fit the screen
   */
    size() {
      switch (this.$vuetify.breakpoint.name) {
        case 'xs': return "display-1"
        case 'sm': return "display-2"
        case 'md': return "display-2"
        case 'lg': return "display-3"
        case 'xl': return "display-3"
      }
      return ""
    }
    
  mounted() {
    if (!this.currentUser) {
      this.$router.push("/login");
    }
    this.computers.pop()
    this.getComputers()
  }

  /**
   * @vuese
   * Used to get the color of the computer based on if it is online or not to return a string representing the color
   * @arg The argument is a boolean representing if it is online or not
   */
  getColor(online: boolean){
    if(online)
      return "green"
    else
      return "red"
  }

  /**
   * @vuese
   * Used to get the computers available for the current user
   */
    getComputers(){
      this.computers.length = 0
      if (this.currentUser && this.currentUser.roles) {
            ComputerService.getAvailableComputersForUser(this.currentUser.username).then(
                  (response) => {
                    if(response.data.length == 0)
                      this.message = "No computers assigned yet"
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
                      this.computers.push(computer)
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
    }

    savePrograms(programs : any){
      //Needs to be in here for some reason, dont delete
      return
    }

  /**
   * @vuese
   * Used to temporary store the time and day we want to power a computer
   * @arg The argument is an object containing the computer that we want to configure and the days and time we want to power it
   */
    saveTime(values : any){
      this.timeMap.set(values.id,{time : values.time,days : values.days})
    }

  /**
   * @vuese
   * Used to send the magic package to try to wake up a computer or to schedule the power up in case we have time and days data,
   * also we set the programs that need to run when the computers turns on
   * @arg The argument is a computer
   */
    powerComputer(computer : Computer){
      if (this.currentUser && this.currentUser.roles) {
        if(computer.selectedPrograms.length>0){
          ProgramService.addProgramForNextPowerUp(computer.selectedPrograms,computer.mac).then(
            (response) => {
              this.message = response.data
            },
            (error) => {
              this.message =
                (error.response && error.response.data && error.response.data.message) ||
                error.message ||
                error.toString();
            }
          );
        }
        var computerId = computer.id;
        var username = this.currentUser.username
        try {
          var days = this.timeMap.get(computer.id).days
          var time = this.timeMap.get(computer.id).time
        } catch (error) {
          this.message = error
        }
        if(days && time){
          ComputerService.schedulePowerOn(computerId,username,days,time).then(
            (response) => {
              this.message = response.data
            },
            (error) => {
              this.message =
                (error.response && error.response.data && error.response.data.message) ||
                error.message ||
                error.toString();
            }
          );
        }
        else{
          ComputerService.tryToPowerComputerOn(computer.mac,username).then(
            (response) => {
              this.message = response.data
            },
            (error) => {
              this.message =
                (error.response && error.response.data && error.response.data.message) ||
                error.message ||
                error.toString();
            }
          );
        }
      }
    }
}
</script>
