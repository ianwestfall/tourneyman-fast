import Vue from 'vue';

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootswatch/dist/superhero/bootstrap.min.css';

import App from './App.vue';
import router from './router';
import store from './store';

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

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
