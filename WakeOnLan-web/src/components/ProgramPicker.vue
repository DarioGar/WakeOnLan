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

@Component({
  name: 'ProgramPicker'
})
// @vuese
// This components allows the user to choose programs to run when the computers powers on
  export default class ProgramPicker extends Vue{
  private programs = [{}]
  private message = ""
    
  created(){
    this.programs.length = 0
    this.getPrograms()
  }

  /**
   * @vuese
   * Used to get the programs allowed on the computer
   */
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

  // The computer that will run the programs selected
  @Prop() computer: any

  // It emits to the parent component the programs that have to run
  @Emit()
    emitPrograms(programs : any) {
      programs = this.programs
  }


}
</script>
