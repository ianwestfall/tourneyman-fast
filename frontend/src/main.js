import Vue from 'vue';

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootswatch/dist/darkly/bootstrap.min.css';

import App from './App.vue';
import router from './router';
import store from './store';
import tournamentStatusFilter from './filters/tournamentStatus.filter';
import competitorDisplayFilter from './filters/competitor.filter';

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

Vue.filter('tournamentStatus', tournamentStatusFilter);
Vue.filter('competitorDisplay', competitorDisplayFilter);

Vue.config.productionTip = false;

document.title = 'TourneyMan';

// Secure any route with meta.auth set to true.
router.beforeEach((to, from, next) => {
  const { loggedIn } = store.state.auth.status;
  if (to.meta.auth && !loggedIn) {
    next('/login');
  } else {
    next();
  }
});

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
