import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
});

import { Framework } from 'vuetify'

declare module 'vue/types/vue' {
  interface Vue {
    $vuetify: Framework
  }
}