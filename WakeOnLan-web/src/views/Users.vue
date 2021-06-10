<template>
  <v-app>  
    <v-main>
          <UserTable/>
    </v-main>
  </v-app>  
</template>

<script lang="ts">
import UserTable from '../components/UserTable.vue'
import { Component, Vue } from "vue-property-decorator";
import { namespace } from "vuex-class";
const Auth = namespace("Auth");

@Component({components:{
      UserTable
    }
})
export default class Users extends Vue{

  @Auth.State("user")
  private currentUser!: any;

  created(){
    if (this.currentUser && this.currentUser.roles) {
        if(!(this.currentUser.roles.includes("admin"))) {
          this.$router.push("/home");
        }
    }
  }

}
</script>