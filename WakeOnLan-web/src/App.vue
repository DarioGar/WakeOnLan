<template>
  <v-app >
    <Navbar></Navbar>
    <v-content class="grey lighten-2">
      <router-view></router-view>
    </v-content>
        
  </v-app>
</template>

<script>
  import Vue from 'vue'
  import Navbar from '@/components/Navbar'

export default Vue.extend({
  name: 'App',
  components: {Navbar}
});
</script>
