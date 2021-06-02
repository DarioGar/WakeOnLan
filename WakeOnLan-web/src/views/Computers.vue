<template>
  <v-container>
    <span>
      Select programs to launch, time and days to power up the computer and hit the power button or, alternatively just hit the power button to turn the computer on now
    </span>
    <span class="red--text">{{message}}</span>
    <v-row class="my-5">
      <v-col class="my-2"
        v-for="(computer,i) in computers"
        :key="i"
        cols="4" sm="4" md="3" xl=3
      >
      <!--Añadir Si alguien ya lo ha arrancado aparezca disabled-->
        <v-card >
          <v-row>
            <v-col cols="1" sm="2" md="2" xl="3">
              <v-icon :class="size()">mdi-desktop-classic</v-icon>
            </v-col>
            <v-col>
              <v-card-title class="text-capitalize">{{computer.os}}</v-card-title>
              <v-card-text>{{computer.ip}}</v-card-text>
            </v-col>
          </v-row>
          <v-card-actions class="mx-5">
            <v-btn @click="computerClicked(computer.id);computer.reveal = !computer.reveal ">
              More
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn @click="powerComputer(computer)">
              <v-icon color="green">
                mdi-power
              </v-icon>
            </v-btn>
          </v-card-actions>
              <v-expand-transition>
                <v-card
                  v-if="computer.reveal"
                  class="transition-fast-in-fast-out v-card--reveal mt-3"
                  style="height: 100%;"
                >
                <ProgramPicker v-bind ='{computer : computer}' v-on:emit-programs="savePrograms"/>
                <PowerOnComponent v-bind ='{computer : computer}' v-on:emit-time="saveTime"/>
                </v-card>
              </v-expand-transition>
        </v-card>
      </v-col>
    </v-row> 
  </v-container>
</template>

<script lang = "ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import { namespace } from "vuex-class";
import vuetify from "vuetify"
import ComputerService,{Computer} from "../services/ComputerService";
const Auth = namespace("Auth");
import ProgramPicker from '../components/ProgramPicker.vue'
import PowerOnComponent from '../components/PowerOnComponent.vue'


@Component({components:{
      ProgramPicker,
      PowerOnComponent
    }
})
  export default class Computers extends Vue{
    private selectedId = -1
    private computers : Computer[] = []
    private message = {}
    //Will store the selected programs in the v-select
    private programsToLaunch = []
    
    private timeMap = new Map()

    @Auth.Getter
    private isLoggedIn!: boolean;

    @Auth.State("user")
    private currentUser!: any;

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

    getComputers(){
      this.computers.length = 0
      if (this.currentUser && this.currentUser.roles) {
            ComputerService.getAvailableComputersForUser(this.currentUser.username).then(
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
                        selectedPrograms : []
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

    computerClicked(pc : number){
      this.selectedId = pc;
    }
    savePrograms(programs : any){
      return
    }
    saveTime(values : any){
      this.timeMap.set(values.id,{time : values.time,days : values.days})
    }

    powerComputer(computer : Computer){
      if (this.currentUser && this.currentUser.roles) {
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
