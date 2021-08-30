<template>
    <nav>
        <v-app-bar class="grey darken-2" flat app>
            <v-app-bar-nav-icon class="grey-text" @click="drawer = !drawer"></v-app-bar-nav-icon>
            <v-img
                class="mx-5"
                position="left"
                contain
                height=5vh
                src="../assets/logo.png"
            ></v-img>
            <v-spacer></v-spacer>
            <v-btn text color="grey" @click="logOut">
                <span>{{loginMessage()}}</span>
                <v-icon>mdi-account-arrow-right-outline</v-icon>
            </v-btn>
        </v-app-bar>

        <v-navigation-drawer app v-model="drawer" class="indigo">
            <v-list>
                <v-list-item  v-for="link in getLinks()" :key="link.text" router :to="link.route">
                    <v-list-item-action>
                        <v-icon class="white--text">{{link.icon}}</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title class="white--text">{{link.text}}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>
    </nav>
</template>

<script lang = "ts">
import { Component, Vue } from "vue-property-decorator";
import { namespace } from "vuex-class";
const Auth = namespace("Auth");

@Component({
  name: 'NavBar'
})
// @vuese
// The navigation top and side bar
export default class NavBar extends Vue {
    drawer = false;
    loggedInlinks = [
        {icon: 'mdi-login',text: 'Login', route: '/login'},
        {icon: 'mdi-account',text: 'Users', route: '/user'},
        {icon: 'mdi-power',text: 'Power On', route: '/computers'},
        {icon: 'mdi-desktop-classic',text: 'My Computers', route: '/pc'},
        {icon: 'mdi-account-multiple',text: 'My Groups', route: '/groups'},
        {icon: 'mdi-home-city',text: 'Rooms', route: '/rooms'},
        {icon: 'mdi-chart-areaspline',text: 'Charts', route: '/charts'}
    ];
    link = [
        {icon: 'mdi-login',text: 'Login', route: '/login'},
    ];

    @Auth.State("user")
    private currentUser!: any;

    @Auth.Action
    private signOut!: () => void;

  /**
   * @vuese
   * Used to get the data for the navigation side bar
   */
    getLinks() {
        if (this.currentUser && this.currentUser.roles)
                return this.loggedInlinks
        return this.link
    }

  /**
   * @vuese
   * Used to change the login button text to login or logout
   */
    loginMessage(){
        if (this.currentUser && this.currentUser.roles)
                return "logout"
        else
                return "login"
    }

    logOut() {
    this.signOut();
    this.$router.push("/login");
  }
}

</script>