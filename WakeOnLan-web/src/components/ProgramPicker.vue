<template>
<v-container fluid>
    <v-select
      v-model="computer.selectedPrograms"
      :items="programs"
      @input="emitPrograms"
      label="Programs(optional)"
      multiple
    >
    </v-select>
  </v-container>
</template>

<script lang="ts">
import { Component, Emit, Prop, Vue } from "vue-property-decorator";
import { namespace } from "vuex-class";
import ProgramService from "../services/ProgramService"

const Auth = namespace("Auth");

@Component
  export default class ProgramPicker extends Vue{
  private programs = [{}]
  private message = ""
    
  created(){
    this.programs.length = 0
    this.getPrograms()
  }

  getPrograms() {
    ProgramService.getPrograms(this.computer.mac).then(
      (response) => {
        response.data.forEach((element: any) => {
          this.programs.push(element[2])
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

  @Prop() computer: any


  @Emit()
    emitPrograms(programs : any) {
      programs = this.programs
  }


}
</script>
