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
          <v-row justify="center" class="my-5">
            <v-col>
              <v-img
                  class="mx-5"
                  position="center"
                  contain
                  height=20vh
                  src="../assets/logo.png"
              ></v-img>
            </v-col>
            <v-col cols=12 class="px-10">
              <v-text-field class="mt-2"
              v-model="user.username"
              :rules = "[rules.required, rules.counter]"
              @keydown.enter="handleLogin"
              label="Username"
              outlined
              ></v-text-field>
            </v-col>
            <v-col cols=12 class="px-10">
              <v-text-field class="mt-2"
              v-model="user.password"
              @keydown.enter="handleLogin"
              :rules = "[rules.required, rules.counter]"
              :type = "'password'"
              label="Password"
              outlined
              ></v-text-field>
            </v-col>
            <v-col cols=12 class="px-10 d-flex justify-end">
              <v-btn @click="handleLogin">
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
import { Component, Vue } from "vue-property-decorator";
import VueRouter from 'vue-router'
import { namespace } from "vuex-class";
const Auth = namespace("Auth");

@Component
  export default class LoginComponent extends Vue{
  private user: any = { username: "", password: "" };
  private message = "";
  private rules =  {
    required: (value: any) => !!value || 'Required.',
    counter: (value: any) => value.length <= 20 || 'Max 20 characters',
  }
          


  @Auth.Getter
  private isLoggedIn!: boolean;

  @Auth.Action
  private login!: (data: any) => Promise<any>;

  created() {
    if (this.isLoggedIn) {
      this.$router.push("/home" );
    }
  }

  handleLogin() {
    if (this.user.username && this.user.password) {
      this.login(this.user).then(
        (data) => {
          this.$router.push("/home");
        },
        (error) => {
          this.message = error;
        }
      );
    }
  }
}
</script>
