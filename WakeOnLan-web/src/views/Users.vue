<template>
  <v-app>  
    <v-main>
          <AdminUserTable v-if="checkAdmin()"/>
          <RegularUserTable v-else/>
    </v-main>
  </v-app>  
</template>

<script lang="ts">
import AdminUserTable from '../components/AdminUserTable.vue'
import RegularUserTable from '../components/RegularUserTable.vue'
import { Component, Vue } from "vue-property-decorator";
import { namespace } from "vuex-class";
const Auth = namespace("Auth");

@Component({components:{
      AdminUserTable,
      RegularUserTable
    }
})
export default class Users extends Vue{

  @Auth.State("user")
  private currentUser!: any;

  checkAdmin(){
      if (this.currentUser && this.currentUser.roles) {
        if((this.currentUser.roles.includes("admin"))) {
          return true
        }
        else return false
      }
  }
}
</script>