<template>
  <v-row justify="center" class="mt-3">
    <v-col cols="8">
      <Invitations/>
      <GroupList/>
    </v-col>
  </v-row>
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
  },
  name : 'Groups'
})
// @vuese
// View that handles the groups on the system
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