<template>
    <UserTable/>
</template>

<script lang="ts">
import UserTable from '../components/UserTable.vue'
import { Component, Vue } from "vue-property-decorator";
import { namespace } from "vuex-class";
const Auth = namespace("Auth");

@Component({components:{
      UserTable
    },
    name : 'Users'
})
// @vuese
// View that handles the users
export default class Users extends Vue{

}
</script>