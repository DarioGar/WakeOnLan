<template>
      <LoginComponent/>
</template>

<script lang="ts">
import LoginComponent from '../components/LoginComponent.vue'
import {Component,Vue} from "vue-property-decorator";

@Component({
  components:{
    LoginComponent,
  },
  name : 'Login'
})
// @vuese
// View that handles the login
export default class Login extends Vue {

}
</script>
