import User from '../models/user';
import AuthService from '../services/auth.service';

const initialUser = JSON.parse(localStorage.getItem('user'));
const initialUserToken = JSON.parse(localStorage.getItem('userToken'));

const initialState = (initialUser && initialUserToken)
  ? { status: { loggedIn: true }, user: new User(initialUser.email), userToken: initialUserToken }
  : { status: { loggedIn: false }, user: null, userToken: null };

export default {
  namespaced: true,
  state: initialState,
  actions: {
    login({ commit }, user) {
      return AuthService.login(user).then(
        (userToken) => {
          const safeUser = new User(user.email);
          commit('loginSuccess', safeUser, userToken);
          return Promise.resolve(safeUser);
        },
        (error) => {
          commit('loginFailure');
          return Promise.reject(error);
        },
      );
    },
    logout({ commit }) {
      AuthService.logout();
      commit('logout');
    },
    register({ commit }, user) {
      return AuthService.register(user).then(
        (response) => {
          commit('registerSuccess');
          return Promise.resolve(response.data);
        },
        (error) => {
          commit('registerFailure');
          return Promise.reject(error);
        },
      );
    },
  },
  mutations: {
    loginSuccess(state, user, userToken) {
      state.status.loggedIn = true;
      state.user = user;
      state.userToken = userToken;
    },
    loginFailure(state) {
      state.status.loggedIn = false;
      state.user = null;
      state.userToken = null;
    },
    logout(state) {
      state.status.loggedIn = false;
      state.user = null;
      state.userToken = null;
    },
    registerSuccess(state) {
      state.status.loggedIn = false;
    },
    registerFailure(state) {
      state.status.loggedIn = false;
    },
  },
};
