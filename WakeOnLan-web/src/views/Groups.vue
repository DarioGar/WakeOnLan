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
@Component({
  components:{
    Invitations,
    GroupList
  }
})
export default class Group extends Vue {

    myGroups(){
      // Obtener los grupos de los que se es miembro
      return "Ninguno"
    }
}
</script>