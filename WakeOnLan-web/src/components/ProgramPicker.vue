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

const Auth = namespace("Auth");

@Component
  export default class ProgramPicker extends Vue{
  programs = [
    'Word',
    'Visual Studio Code',
    'Visual Paradigm',
    'Unity'
      ]
    
  created(){
    this.getPrograms()
  }

  getPrograms() {
    throw new Error("Method not implemented.");
  }

  @Prop() computer: any


  @Emit()
    emitPrograms(programs : any) {
      programs = this.programs
  }


}
</script>
