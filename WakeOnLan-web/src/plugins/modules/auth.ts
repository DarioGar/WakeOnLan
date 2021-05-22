import { authService } from '@/api'

const namespaced = true;

const state = {
  user: {},
  isLoggedIn: false
};

const getters = {
  isLoggedIn: (state: { isLoggedIn: any; }) => state.isLoggedIn,
  user: (state: { user: any; }) => state.user
};

const actions = {
  async registerUser({ dispatch }: any, user: any) {
    await authService.post('/register', user)
    await dispatch('fetchUser')
  },
  async loginUser({ dispatch }: any, user: any) {
    await authService.post('/login', user)
    await dispatch('fetchUser')
  },
  async fetchUser({ commit }: any) {
    await authService.get('/user')
      .then(({ data }) => commit('setUser', data))
  },
  async logoutUser({ commit } : any) {
    await authService.post('/logout');
    commit('logoutUserState');
  }
};

const mutations = {
  setUser(state: { isLoggedIn: boolean; user: any; }, user: any) {
    state.isLoggedIn = true;
    state.user = user;
  },
  logoutUserState(state: { isLoggedIn: boolean; user: {}; }) {
    state.isLoggedIn = false;
    state.user = {};
  }
};

export default {
  namespaced,
  state,
  getters,
  actions,
  mutations
};