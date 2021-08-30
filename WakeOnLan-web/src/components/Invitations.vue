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
                  <span>From: {{invitation.sender}} at: {{invitation.time}}</span>
                    <v-spacer></v-spacer>
                    <v-btn @click="acceptInvitation(invitation)">
                        Accept
                    </v-btn>
                    <v-btn @click="refuseInvitation(invitation)">
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
import GroupService from "../services/GroupService";
const Auth = namespace("Auth");

@Component({
  name: 'Invitations'
})
// @vuese


export default class Invitations extends Vue{
    private message = ""
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

  /**
   * @vuese
   * Used to get the invitations if there are any for the current user
   */
    getInvitations(){
      GroupService.getInvitationsFor(this.currentUser.username).then(
        (response) => {
            response.data.forEach((element : any) => {
              if(element[4]=='on hold'){
                var invitation = {
                  id : element[0],
                  sender : element[1],
                  receiver : element[2],
                  time : element[5],
                  work_group : element[3]
                }
                this.invitations.push(invitation)
              }

          });
        },
        (error) => {
          this.message =
            (error.response && error.response.data && error.response.data.message) ||
            error.message ||
            error.toString();
          }
      )
    }

  /**
   * @vuese
   * Used to accept an invitation to a group
   * @arg The argument is an invitation
   */
    acceptInvitation(inv : any){
      var id = inv.id
      var groupId = inv.work_group
      var userId = inv.receiver
      GroupService.accept(id,groupId,userId)
      this.$router.push('/groups')
    }

  /**
   * @vuese
   * Used to refuse an invitation to a group
   * @arg The argument is an invitation
   */
    refuseInvitation(inv : any){
      var id = inv[0]
      GroupService.deny(id)
      this.$router.push('/groups')
    }
}
</script>
