<template>
  <v-row>

    <v-dialog
      v-model="dialog"
      persistent
      max-width="600px"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          dark
          v-bind="attrs"
          v-on="on"
          @click="computer = defaultcomputer"
        >
          New Computer
        </v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="text-h5">Computer Data</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  label="MAC*"
                  :disabled="editing"
                  v-model="computer.mac"
                  required
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="4"
                md="4"
              >
                <v-text-field
                  label="IP"
                  v-model="computer.ip"
                  hint="used to check if its online"
                  persistent-hint
                ></v-text-field>
              </v-col>
              <v-col cols="2">
                <v-text-field
                  label="RAM"
                  v-model="computer.ram"
                  suffix="GB"
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
              >
                <v-text-field
                  label="Name"
                  v-model="computer.name"
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
              >
                <v-text-field
                  label="CPU"
                  v-model="computer.cpu"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  label="GPU"
                  v-model="computer.gpu"
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="5"
              >
                <v-select
                  :items="['windows', 'linux', 'macos', 'other']"
                  label="Operating System"
                  v-model="computer.os"
                ></v-select>
              </v-col>
              <v-col
              cols="1">
                <v-checkbox 
                label="SSD"
                v-model="computer.ssd">
                </v-checkbox>
              </v-col>
              <v-col cols="12">
                <small>*click a path to remove it</small>
                <v-combobox
                v-model="comboText"
                @input.native="comboText=$event.srcElement.value"
                solo
                :search-input.sync="searchString"
                :disabled="!editing"
                :items="computer.selectedPrograms"
                @keydown.enter="handleProgram(computer)"
                label="Write the path to the programs you want to register and hit enter"
                @change="deleteProgram(computer,$event)"
                >
                
              </v-combobox>
              
              </v-col>
            </v-row>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-btn
            color="error"
            text
            :disabled="!editing"
            @click="deleteComputer(computer)"
          >
            Delete
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="close()"
          >
            Close
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="saveComputer(computer)"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script lang = "ts">
import { Component, Vue,Prop } from "vue-property-decorator";
import { namespace } from "vuex-class";
import ComputerService from "../services/ComputerService"
import ProgramService from "../services/ProgramService"
const Auth = namespace("Auth");

@Component({
  name: 'ComputerDialog'
})
// @vuese
export default class ComputerDialog extends Vue {


  private message = {}
  private editing = false
  private searchString = ""
  private comboText = ""
  private defaultcomputer = {ip : "",name: "",mac : "",cpu : "",ram : 8,ssd : false,os : "Windows",gpu : "",use: "",selectedPrograms: []}
  private computer = {ip : "",name: "",mac : "",cpu : "",ram : 8,ssd : false,os : "Windows",gpu : "",use: "",selectedPrograms: []}

  // The computer that we are editing if any has been given
  @Prop() edit : any
  // The dialog that controls if this component is showing or not
  @Prop() dialog : any

  @Auth.State("user")
    private currentUser!: any;

  /**
   * @vuese
   * Used to change the funcionalty from editing to new computer and vice versa
   */
  updated(){
    if(Object.keys(this.edit).length){
      this.computer = this.edit
      this.editing = true
    }
    else{
      this.computer = this.defaultcomputer
      this.editing = false
    }
      return
  }

  /**
   * @vuese
   * Used to open the component with the funcionalty of editing or new computer
   */
  mounted(){
    if(Object.keys(this.edit).length){
      this.computer = this.edit
      this.editing = true
    }
    else{
      this.computer = this.defaultcomputer
      this.editing = false
    }
    return
  }

  /**
   * @vuese
   * Used to add a program to the computer programs list
   * @arg The argument is a computer
   */
  handleProgram(computer : any){
      if(this.comboText!= "")
        computer.selectedPrograms.push(this.comboText)
      this.message = computer.selectedPrograms
      this.searchString = ""
      return
  }

  /**
   * @vuese
   * Used to remove a program to the computer programs list
   * @arg The argument is a computer
   */
  deleteProgram(computer : any,event : any){
    var index = -1
    if ((index = computer.selectedPrograms.indexOf(event)) > -1)
      computer.selectedPrograms.splice(index,1)
      this.searchString = ""
      this.comboText = ""
  }

  /**
   * @vuese
   * Used to close this dialog
   */
  close(){
    this.dialog = false
    this.edit = {}
    this.editing = false
  }

  /**
   * @vuese
   * Used to save the newly created computer to the database making a call to the API or edit a given computer depending on the mode this component is working
   * @arg The argument is a computer
   */
  saveComputer(computer : any){
    if(!this.editing){
      ComputerService.registerNew(computer.mac,computer.ip,computer.ram,computer.cpu,computer.gpu,computer.os,computer.ssd,this.currentUser.username,computer.name).then(
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
      ComputerService.update(computer.mac,computer.ip,computer.ram,computer.cpu,computer.gpu,computer.os,computer.ssd,computer.name).then(
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
    if(computer.selectedPrograms.length > 0)
    ProgramService.updatePrograms(computer.selectedPrograms,computer.mac).then(
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
    this.changeAllowed(this.currentUser.username,true,computer.mac)
    this.edit = {}
    window.location.reload()
  }

  /**
   * @vuese
   * Used to remove a computer from the system
   * @arg The argument is a computer
   */
  deleteComputer(computer : any){
    ComputerService.delete(computer.mac).then(
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
    window.location.reload()
    this.dialog = false
  }

  /**
   * @vuese
   * Used to change the permissions of a user to allowed or disallowed
   * @arg The first argument is a string representing the user who is to be changed
   * @arg The second argument is a boolean representing if the user is allowed(true) or not(false)
   * @arg The third argument is a string representing the mac of the computer that we want to allow access or not
   */
  changeAllowed(username: string,allowed:boolean,mac : string){
    ComputerService.changeAllowance(username,allowed,mac).then(
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