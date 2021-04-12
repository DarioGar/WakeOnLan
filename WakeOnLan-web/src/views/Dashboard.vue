<template>
  <div class="dashboard">
    <v-container class="my-5">
      <h1 class="subheading grey--text">Dashboard</h1>
      <v-card flat class="pa-3 grey darken-1" v-for="computer in computers" :key="computer.mac">
        <v-row :class="`computer ${computer.ssd}`">
          <v-col cols="3" md="3">
            <div class="caption grey--text"> MAC </div>
            <div class="text-uppercase">{{computer.mac}}</div>
          </v-col>
          <v-col cols="7" sm="6" md="3">
            <div class="caption grey--text"> CPU </div>
            <div>{{computer.cpu}}</div>
          </v-col>
          <v-col cols="2" sm="1" md="1">
            <div class="caption grey--text"> RAM </div>
            <div>{{computer.ram}}</div>
          </v-col>
          <v-col cols="12" sm="10" md="5">
            <div class="caption grey--text"> GPU </div>
            <div>{{computer.gpu}}</div>
          </v-col>
        </v-row>
        <v-divider></v-divider>
      </v-card>
     </v-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';


export default {
  data() {
    return {
      computers: [
        {mac : "ff:ff:ff:ff:ff:01",cpu: "AMD Ryzen 7 3700X", ram: 32,gpu: "NVIDIA GeForce RTX 2070 SUPER",ssd: true,os:"Windows"},
        {mac : "ff:ff:ff:ff:ff:02",cpu: "AMD Ryzen 5 3600", ram: 16,gpu: "NVIDIA GeForce RTX 2060",ssd: false,os:"Linux"},
        {mac : "ff:ff:ff:ff:ff:03",cpu: "Intel Core i7-9700K", ram: 32,gpu: "NVIDIA GeForce GTX 1660 SUPER",ssd: true,os:"MAC"},
        {mac : "ff:ff:ff:ff:ff:04",cpu: "Intel Core i5-9600K", ram: 16,gpu: "AMD Radeon RX 580",ssd: false,os:"BSDOS"}
      ]
    }
  }
}
</script>

<style scoped>

.computer.true{
  border-left: 4px solid lime
}
.computer.false{
  border-left: 4px solid red
}

</style>