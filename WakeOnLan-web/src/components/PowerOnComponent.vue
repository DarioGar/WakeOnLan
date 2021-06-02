<template>
  <v-container >
      <v-menu
        ref="menu"
        v-model="menu2"
        :close-on-content-click="false"
        :nudge-right="40"
        :return-value.sync="time"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="290px"
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

        <v-time-picker
          v-if="menu2"
          v-model="time"
          full-width
          @click:minute="$refs.menu.save(time)"
          :allowed-minutes="allowedStep"
          @input="emitTime"
        >
        </v-time-picker>
          <v-select
          v-model="powerOnDays"
          :items="days"
          label="Days to power on"
          dense
          :input="emitTime(this.time)"
          multiple
          ></v-select>
      </v-menu>
  </v-container>
  
</template>

<script lang="ts">
import { Component, Emit, Prop, Vue } from "vue-property-decorator";
import VueRouter from 'vue-router'
import { namespace } from "vuex-class";
const Auth = namespace("Auth");

@Component
  export default class PowerOnComponent extends Vue{
  time =  null
  menu2 = false
  days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
  powerOnDays = []
  allowedStep(m : any){
    return m % 15 === 0
  }  

  @Auth.Getter
  private isLoggedIn!: boolean;

  @Prop() computer: any

  @Emit()
    emitTime(time : any) {
      var id = this.computer.id
      var days = this.powerOnDays
      return {id,time,days}
  }

}
</script>
