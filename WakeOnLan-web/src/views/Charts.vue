<template>
  <v-row align="center" justify="space-around" class="mx-4 mt-5">
    <v-col cols="3" align="center">
      <h2>Computers powered each day</h2>
      <DaysChart :chartData="{}" :options="{}"></DaysChart>
    </v-col>
    <v-col cols="3" align="center">
      <h2>Time running</h2>
      <TimeRunningChart  :chartData="{}" :options="{}"></TimeRunningChart>
    </v-col>
    <v-col cols="3" align="center">
      <h2>Times each user has powered on a computer</h2>
      <ActiveUsersChart  :chartData="{}" :options="{}"></ActiveUsersChart>
    </v-col>
    
  </v-row>
    
    
</template>


<script lang= "ts">
  import DaysChart from "../components/DaysChart.vue"
  import TimeRunningChart from "../components/TimeRunningChart.vue"
  import ActiveUsersChart from "../components/ActiveUsersChart.vue"
  import { Component, Vue } from "vue-property-decorator";

  @Component({components:{
    DaysChart,
    TimeRunningChart,
    ActiveUsersChart
  },
  name: 'Charts'})
  // @vuese
  export default class Charts extends Vue {
}
</script>