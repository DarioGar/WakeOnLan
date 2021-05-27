import Vue from 'vue';
import Vuex from 'vuex';
import Auth from "./modules/auth";

Vue.use(Vuex);

export const store = new Vuex.Store({
  modules: {
    Auth
  }
});