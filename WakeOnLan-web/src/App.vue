<template>
  <v-app>
    <Navbar></Navbar>
      <v-content class="">
        <router-view></router-view>
      </v-content>
  </v-app>
</template>

<script>
  import Navbar from '@/components/Navbar'
export default({
  name: 'App',
  components: {Navbar}
});
</script>
