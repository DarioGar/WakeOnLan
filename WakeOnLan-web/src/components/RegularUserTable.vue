<template>
  <v-main>
  <v-row justify="center" class="mx-5">
    <v-dialog
      v-model="information"
      width="500"
    >
      <v-card>
        <v-card-title>
          {{message}}
        </v-card-title>
      </v-card>
    </v-dialog>
    <v-data-table
      :headers="headers"
      :items="users"
      sort-by="username"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar
          flat
        >
          <v-toolbar-title>Users</v-toolbar-title>
          
          <v-divider
            class="mx-4"
            inset
            vertical
          ></v-divider>
          <v-spacer></v-spacer>
          <v-dialog
            v-model="dialog"
            max-width="500px"
          >
            <v-card>
              <v-card-title>
                <span class="headline">{{formTitle()}}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col
                      cols="12"
                      sm="6"
                      md="6"
                    >
                      <v-text-field
                        label="Username*"
                        required
                        v-model="user.username"
                      ></v-text-field>
                    </v-col>
                    <v-col 
                    cols="12"
                    sm="6"
                    md="6">
                      <v-text-field
                        label="Password*"
                        type="password"
                        required
                        v-model="user.password"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        label="Email*"
                        required
                        v-model="user.email"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="4"
                    >
                      <v-select
                        :items="['regular', 'learning', 'project_manager', 'admin']"
                        label="Role*"
                        required
                        v-model="user.role"
                      ></v-select>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        label="Full name"
                        v-model="user.fullname"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="close"
                >
                  Cancel
                </v-btn>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="save"
                >
                  Save
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title class="headline">Are you sure you want to delete this item?</v-card-title>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
                <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <!--Actions-->
      <template v-slot:[`item.invitations`]="{ item }">
        <v-menu offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-icon
              icon
              v-bind="attrs"
              v-on="on"
            >
              mdi-account-multiple-plus
            </v-icon>
          </template>
          <v-list>
            <v-list-item
              v-for="(workgroup, index) in workGroups"
              :key="index"
              link
              @click="sendInvite(item.username,workgroup.id)"
            >
              {{ workgroup.name }}
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
      <template v-slot:no-data>
        <v-btn
          color="primary"
          @click="getUsers"
        >
          Reset
        </v-btn>
      </template>
      
    </v-data-table>
  </v-row>
  </v-main>
</template>

<script lang = "ts">

import { Component, Vue, Watch } from "vue-property-decorator";
import { namespace } from "vuex-class";
import UserService from "../services/UserService";
import GroupService from "../services/GroupService"
const Auth = namespace("Auth");

@Component
  export default class RegularUsers extends Vue{
    private dialog =  false
    private submitted = false;
    private message = "";
    private information = false;
    private headers = [
        {
        text: 'Username',
        align: 'start',
        value: 'username',
        },
        { text: 'Email', value: 'email' },
        { text: 'Invite', value: 'invitations', sortable: false }
    ]
    private users = [{}]
    private workGroups = [{}]
    private editedIndex = -1
    private user = {username:"",email:"",role:"",fullname:"",password:""}
    formTitle () : any {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
    }

    @Auth.Getter
    private isLoggedIn!: boolean;

    @Auth.Action
    private register!: (data: any) => Promise<any>;

    @Auth.State("user")
    private currentUser!: any;

    mounted() {
      this.users.pop()
      this.getUsers()
      this.workGroups.pop()
      this.getWorkGroup()
    }

    sendInvite(to:string,group:number){
      GroupService.sendInvite(this.currentUser.username,to,group,).then(
        (response) => {
          response.data
          this.message = "Invitación enviada a " + to
          this.information=true;
        },
        (error) => {
          this.message =
            (error.response && error.response.data && error.response.data.message) ||
            error.message ||
            error.toString();
            this.information=true;
          }
      )
    }

    getWorkGroup(){
      this.workGroups.length = 0
      GroupService.getWorkGroup(this.currentUser.username).then(
        (response) => {
          response.data.forEach((element : any) => {
            var workGroup = {
              id : element[0],
              user_id : element[1],
              name : element[2],
              path : element[3],
              department : element[4]
            }
            this.workGroups.push(workGroup)
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

    getUsers () {
      this.users.length = 0
      UserService.getUsers().then(
      (response) => {
        response.data.forEach((element: any) => {
          var user = {
            username : element[0],
            email : element[1],
            role : element[2],
            password : element[3],
            fullname : element[4]
          }
          this.users.push(user)
        });
      },
      (error) => {
        this.message =
          (error.response && error.response.data && error.response.data.message) ||
          error.message ||
          error.toString();
      }
    );
    }
  }
</script>