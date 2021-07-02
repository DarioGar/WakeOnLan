<template>
  <div class="about">
    <v-container class="my-5">
      <Invitations/>
      <GroupList/>
    </v-container>
  </div>
</template>


<script lang="ts">
import {Component,Vue} from "vue-property-decorator";
import Invitations from '../components/Invitations.vue'
import GroupList from '../components/GroupList.vue'
import { namespace } from "vuex-class";
const Auth = namespace("Auth");
@Component({
  components:{
    Invitations,
    GroupList
  }
})
export default class Group extends Vue {
  

  @Auth.State("user")
  private currentUser!: any;

  mounted() {
    if (!this.currentUser) {
      this.$router.push("/login");
    }
  }
}
</script>