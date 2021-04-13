<template>
    <nav>
        <v-app-bar class="grey darken-2" flat app>
            <v-app-bar-nav-icon class="grey-text" @click="drawer = !drawer"></v-app-bar-nav-icon>
            <v-app-bar-title class="text grey--text">
                <span class="font-weight-light">wake</span>
                <span >OnLan</span>
            </v-app-bar-title>

            <v-btn text color="grey">
                <span>Sign out</span>
                <v-icon>mdi-account-arrow-right-outline</v-icon>
            </v-btn>
        </v-app-bar>

        <v-navigation-drawer app v-model="drawer" class="indigo">
            <v-list>
                <v-list-item  v-for="link in links" :key="link.text" router :to="link.route">
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

<script>
export default {
    data() {
        return {
            drawer: false,
            links: [
                {icon: 'mdi-view-dashboard',text: 'DashBoard', route: '/'},
                {icon: 'mdi-laptop',text: 'Computers', route: '/computers'},
                {icon: 'mdi-account-multiple',text: 'My Groups', route: '/groups'}
            ]
        }
    }
}

</script>