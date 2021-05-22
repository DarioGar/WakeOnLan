<template>
  <v-app>  
    <v-main>
      <LoginComponent/>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import LoginComponent from '../components/LoginComponent.vue'


export default {
  data() {
    return {
      //
    }
  },
  components:{
    LoginComponent
  }
}
</script>
