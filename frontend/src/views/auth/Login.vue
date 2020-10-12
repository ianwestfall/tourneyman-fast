<template>
  <div id="login-container" class="row">
    <b-card header="Login" class="text-center mx-auto" style="width: 50vw;">
      <b-form @submit.prevent="onSubmit">
        <b-form-group label="Email address:" label-for="email" label-cols-md="3">
          <b-form-input
            id="email"
            name="email"
            v-model="user.email"
            type="email"
            required>
          </b-form-input>
        </b-form-group>

        <b-form-group label="Password:" label-for="password" label-cols-md="3">
          <b-form-input
            id="password"
            name="password"
            v-model="user.password"
            type="password"
            required>
          </b-form-input>
        </b-form-group>

        <b-button type="submit" variant="primary" :disabled="loading">
          <span>Login</span>
          <span v-show="loading" class="spinner-border spinner-border-sm"></span>
        </b-button>

        <div v-if="message" class="text-danger">{{ message.detail }}</div>
      </b-form>
    </b-card>
  </div>
</template>

<script>
import User from '../../models/user';

export default {
  name: 'Login',
  data() {
    return {
      user: new User(),
      loading: false,
      message: '',
    };
  },
  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
  },
  created() {
    if (this.loggedIn) {
      this.$router.push('/');
    }
  },
  methods: {
    onSubmit() {
      this.loading = true;
      if (this.user.email && this.user.password) {
        this.$store.dispatch('auth/login', this.user).then(
          () => {
            this.$router.push('/');
          },
          (error) => {
            console.error('Error logging in');
            this.loading = false;
            this.message = (error.response && error.response.data)
              || error.message
              || error.toString();
            console.error(this.message);
          },
        );
      }
    },
  },
};
</script>

<style scoped>
  #login-container {
    margin-top: 25px;
  }
</style>
