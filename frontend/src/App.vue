<template>
  <div id="app">
    <b-container fluid>
    <div>
      <b-navbar toggleable="lg" type="dark" class="bg-dark">
        <b-navbar-brand to="/">TourneyMan</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item to="/">Home</b-nav-item>
            <b-nav-item to="/about">About</b-nav-item>
          </b-navbar-nav>

          <b-navbar-nav class="ml-auto" v-if="loggedIn">
            <b-nav-item-dropdown right>
              <template v-slot:button-content>
                <em>{{ authenticatedUser }}</em>
              </template>
              <b-dropdown-item to="/profile">Profile</b-dropdown-item>
              <b-dropdown-item @click.prevent="logOut">Log Out</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-navbar-nav>

          <b-navbar-nav class="ml-auto" v-else>
            <b-nav-item to="/login">Login</b-nav-item>
            <b-nav-item to="/register">Register</b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
    <div class="view-container">
      <alerts />
      <router-view/>
    </div>
  </b-container>
  </div>
</template>

<script>
import Alerts from '@/components/alerts/Alerts.vue';

export default {
  name: 'App',
  components: { Alerts },
  computed: {
    loggedIn() {
      return this.$store.getters['auth/loggedIn'];
    },
    authenticatedUser() {
      let username = null;
      const user = this.$store.getters['auth/authenticatedUser'];
      if (user) {
        username = user.getUsername();
      }

      return username;
    },
  },
  methods: {
    logOut() {
      this.$store.dispatch('auth/logout');
      this.$router.push('/login');
    },
  },
  watch: {
    $route(to) {
      document.title = to.meta.title || 'TourneyMan';
    },
  },
};
</script>

<style lang="less" scoped>
.view-container {
  padding: 10px;
}
</style>
