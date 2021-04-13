<template>
      <v-container>
        <v-row>
          <v-col
            v-for="(computer,i) in computers"
            :key="i"
            cols="4" sm="4" md="3" xl=3
          >
            <v-card :to="'/'" hover exact height="200">
              <v-icon class="display-4">mdi-desktop-classic</v-icon>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
</template>

<script lang="ts">


export default {
  data(){
    return{
      computers:[
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
      ]
    }
  }
}
</script>
