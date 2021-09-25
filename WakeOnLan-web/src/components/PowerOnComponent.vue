<template>
  <v-container >
      <v-menu
        ref="menu"
        color="white"
        v-model="menu"
        :close-on-content-click="false"
        :nudge-top="100"
        :return-value.sync="time"
        transition="scale-transition"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            v-model="time"
            label="Select time to power on"
            prepend-icon="mdi-clock-time-four-outline"
            readonly
            v-bind="attrs"
            v-on="on"
          ></v-text-field>
        </template>
        <v-select
        v-model="powerOnDays"
        :items="days"
        background-color="white"
        label="Days to power on"
        :input="emitTime(this.time)"
        multiple
        ></v-select>
        <v-time-picker
          v-if="menu"
          v-model="time"
          no-title
          format="24hr"
          @click:minute="$refs.menu.save(time)"
          :allowed-minutes="allowedStep"
          @input="emitTime"
        >
        </v-time-picker>
      </v-menu>
  </v-container>
  
</template>

<script lang="ts">
import { Component, Emit, Prop, Vue } from "vue-property-decorator";
import VueRouter from 'vue-router'
import { namespace } from "vuex-class";
const Auth = namespace("Auth");

@Component({
  name: 'PowerOnComponent'
})
// @vuese
//This component allows the user to pick days and time to schedule a computer to power up
  export default class PowerOnComponent extends Vue{
  time =  null
  menu = false
  days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
  powerOnDays = []
  allowedStep(m : any){
    return m % 15 === 0
  }  

  @Auth.Getter
  private isLoggedIn!: boolean;
  // The computer that will be configured to power up
  @Prop() computer: any

  // It emits to the parent component the days and time configured
  @Emit()
    emitTime(time : any) {
      var id = this.computer.id
      var days = this.powerOnDays
      return {id,time,days}
  }

}
</script>
