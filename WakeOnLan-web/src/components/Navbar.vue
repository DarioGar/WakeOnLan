<template>
    <nav>
        <v-app-bar class="grey darken-2" flat app>
            <v-app-bar-nav-icon class="grey-text" @click="drawer = !drawer"></v-app-bar-nav-icon>
            <v-app-bar-title class="text grey--text mx-5">
                <span class="font-weight-light">wake</span>
                <span >OnLan</span>
            </v-app-bar-title>
            <v-spacer></v-spacer>
            <v-btn text color="grey" @click="logOut">
                <span>Sign out</span>
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

@Component
export default class NavBar extends Vue {
    drawer = false;
    loggedInlinks = [
        {icon: 'mdi-login',text: 'Login', route: '/login'},
        {icon: 'mdi-account',text: 'Users', route: '/user'},
        {icon: 'mdi-view-dashboard',text: 'DashBoard', route: '/home'},
        {icon: 'mdi-laptop',text: 'Computers', route: '/computers'},
        {icon: 'mdi-account-multiple',text: 'My Groups', route: '/groups'}
    ];
    link = [
        {icon: 'mdi-login',text: 'Login', route: '/login'},
    ];

    @Auth.State("user")
    private currentUser!: any;

    @Auth.Action
    private signOut!: () => void;

    getLinks() {
        if (this.currentUser && this.currentUser.roles) 
                return this.loggedInlinks
        return this.link
    }

    logOut() {
    this.signOut();
    this.$router.push("/login");
  }
}

</script>