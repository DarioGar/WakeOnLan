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
            label="Picker in menu"
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
        ></v-time-picker>
      </v-menu>
  </v-container>
  
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import VueRouter from 'vue-router'
import { namespace } from "vuex-class";
const Auth = namespace("Auth");

@Component
  export default class PowerOnComponent extends Vue{
        time =  null
        menu2 = false

  @Auth.Getter
  private isLoggedIn!: boolean;

  created() {
      return
  }

}
</script>
