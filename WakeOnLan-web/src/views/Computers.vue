<template>
      <v-container>
        <v-row class="my-5">
          <v-col class="my-2"
            v-for="(computer,i) in computers"
            :key="i"
            cols="4" sm="4" md="3" xl=3
          >
          <!--Añadir Si alguien ya lo ha arrancado aparezca disabled-->
            <v-card hover exact>
              <v-row>
                <v-col cols="1" sm="2" md="2" xl="3">
                  <v-icon :class="size">mdi-desktop-classic</v-icon>
                </v-col>
                <v-col>
                  <v-card-title>{{computer.name}}</v-card-title>
                  <v-card-text>{{computer.ip}}</v-card-text>
                  <v-card-action></v-card-action>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
        </v-row> 
      </v-container>
</template>

<script lang="ts">
  import Vue from 'vue'

  export default Vue.extend({
  data: () => ({
      computers:[
        {name:"Mi PC 1",ip:"192.168.1.1",mac : "ff:ff:ff:ff:ff:01",cpu: "AMD Ryzen 7 3700X", ram: 32,gpu: "NVIDIA GeForce RTX 2070 SUPER",ssd: true,os:"Windows",expectedUse:""},
        {name:"Mi PC 2",ip:"192.168.1.2",mac : "ff:ff:ff:ff:ff:02",cpu: "AMD Ryzen 5 3600", ram: 16,gpu: "NVIDIA GeForce RTX 2060",ssd: false,os:"Linux",expectedUse:""},
        {name:"Mi PC 3",ip:"192.168.1.3",mac : "ff:ff:ff:ff:ff:03",cpu: "Intel Core i7-9700K", ram: 32,gpu: "NVIDIA GeForce GTX 1660 SUPER",ssd: true,os:"MAC",expectedUse:""},
        {name:"Mi PC 4",ip:"192.168.1.4",mac : "ff:ff:ff:ff:ff:04",cpu: "Intel Core i5-9600K", ram: 16,gpu: "AMD Radeon RX 580",ssd: false,os:"BSDOS",expectedUse:""},
        {name:"Mi PC 5",ip:"192.168.1.5",mac : "ff:ff:ff:ff:ff:01",cpu: "AMD Ryzen 7 3700X", ram: 32,gpu: "NVIDIA GeForce RTX 2070 SUPER",ssd: true,os:"Windows",expectedUse:""},
        {name:"Mi PC 6",ip:"192.168.1.6",mac : "ff:ff:ff:ff:ff:02",cpu: "AMD Ryzen 5 3600", ram: 16,gpu: "NVIDIA GeForce RTX 2060",ssd: false,os:"Linux",expectedUse:""},
        {name:"Mi PC 7",ip:"192.168.1.7",mac : "ff:ff:ff:ff:ff:03",cpu: "Intel Core i7-9700K", ram: 32,gpu: "NVIDIA GeForce GTX 1660 SUPER",ssd: true,os:"MAC",expectedUse:""},
        {name:"Mi PC 8",ip:"192.168.1.8",mac : "ff:ff:ff:ff:ff:04",cpu: "Intel Core i5-9600K", ram: 16,gpu: "AMD Radeon RX 580",ssd: false,os:"BSDOS",expectedUse:""}
      ]
  }),
    methods: {
    },
    computed:{
      size : function () {
        console.log(this.$vuetify.breakpoint.name)
        switch (this.$vuetify.breakpoint.name) {
          case 'xs': return "display-1"
          case 'sm': return "display-2"
          case 'md': return "display-2"
          case 'lg': return "display-3"
          case 'xl': return "display-3"
        }
        return ""
      },
    }
})
</script>
