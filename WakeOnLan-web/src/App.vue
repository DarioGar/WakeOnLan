<template>
  <v-app >
    <Navbar></Navbar>
    <v-main class="grey lighten-2">
      <router-view></router-view>
    </v-main>
        
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
