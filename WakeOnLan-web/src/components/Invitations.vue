<template>
  <v-container>
      <v-row class="my-2">
          <v-col class="my-2"
            v-for="(invitation,i) in invitations"
            :key="i"
            cols=12
            >
            <v-card >
                <v-card-actions class="mx-5">
                    <span>{{getInvitations()}}</span>
                    <v-spacer></v-spacer>
                    <v-btn>
                        Accept
                    </v-btn>
                    <v-btn>
                        Refuse
                    </v-btn>
                </v-card-actions>
            </v-card>
          </v-col>
      </v-row>

  </v-container>
</template>
    


<script lang = "ts">
import { Component, Vue } from "vue-property-decorator";
import { namespace } from "vuex-class";
const Auth = namespace("Auth");

@Component
export default class Invitations extends Vue{
    private message = {}
    private invitations = [{}]

    @Auth.Getter
    private isLoggedIn!: boolean;

    @Auth.State("user")
    private currentUser!: any;
    
    mounted() {
      if (!this.currentUser) {
        this.$router.push("/login");
      }
      this.invitations.pop()
      this.getInvitations()
    }

    getInvitations(){
        return ""
    }
}
</script>
