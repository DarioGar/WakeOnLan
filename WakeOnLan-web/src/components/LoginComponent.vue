<template>
  <v-container >
    <v-row justify="center" class="mx-5">
      <v-col
        cols="12"
        sm="8"
      >
        <v-sheet
          min-height="40vh"
          rounded="lg"
          class="grey lighten-2 my-10"
        >
          <v-row class="my-5">
            <v-col cols=12 class="px-10">
              <v-text-field class="mt-2"
              v-model="username"
              @keydown.enter="checkData"
              label="Username"
              outlined
              ></v-text-field>
            </v-col>
            <v-col cols=12 class="px-10">
              <v-text-field class="mt-2"
              v-model="password"
              @keydown.enter="checkData"
              :type = "'password'"
              label="Password"
              outlined
              ></v-text-field>
            </v-col>
            <v-col cols=12 class="px-10 d-flex justify-end">
              <v-btn @click="checkData">
                Login
              </v-btn>
            </v-col>
          </v-row>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
  
</template>

<script lang="ts">
  import Vue from 'vue'

  export default Vue.extend({
    name: 'Login',
    data: () => ({
      username : "",
      password : ""
    }),
    methods:{
      checkData(){
        if(!(this.username === "" && this.password === ""))
        this.$router.push("home")
      }
    }
  })
</script>
