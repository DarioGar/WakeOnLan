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
            @click="save(computer)"
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

@Component
export default class ComputerDialog extends Vue {


  private message = {}
  private editing = false
  private searchString = ""
  private comboText = ""
  private defaultcomputer = {ip : "",mac : "",cpu : "",ram : 8,ssd : false,os : "Windows",gpu : "",use: "",selectedPrograms: []}
  private computer = {ip : "",mac : "",cpu : "",ram : 8,ssd : false,os : "Windows",gpu : "",use: "",selectedPrograms: []}
  @Prop() edit : any
  @Prop() dialog : any

  @Auth.State("user")
    private currentUser!: any;

  updated(){
    if(Object.keys(this.edit).length){
      this.computer = this.edit
      this.editing = true
    }
    else{
      this.computer = this.defaultcomputer
      this.editing = false
    }
      
  }

  mounted(){
    if(Object.keys(this.edit).length){
      this.computer = this.edit
      this.editing = true
    }
    else{
      this.computer = this.defaultcomputer
      this.editing = false
    }
  }

  handleProgram(computer : any){
      if(this.comboText!= "")
        computer.selectedPrograms.push(this.comboText)
      this.message = computer.selectedPrograms
      this.searchString = ""
  }

  deleteProgram(computer : any,event : any){
    var index = -1
    if ((index = computer.selectedPrograms.indexOf(event)) > -1)
      computer.selectedPrograms.splice(index,1)
      this.searchString = ""
      this.comboText = ""
  }

  close(){
    this.dialog = false
    this.edit = {}
    this.editing = false
  }

  save(computer : any){
    if(!this.editing){
      ComputerService.registerNew(computer.mac,computer.ip,computer.ram,computer.cpu,computer.gpu,computer.os,computer.ssd,this.currentUser.username).then(
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
      ComputerService.update(computer.mac,computer.ip,computer.ram,computer.cpu,computer.gpu,computer.os,computer.ssd).then(
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
    this.editing = false
    window.location.reload()
  }

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