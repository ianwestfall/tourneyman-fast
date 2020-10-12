<template>
  <div id="register-container" class="row">
    <b-card header="Register" class="text-center mx-auto" style="width: 50vw;">
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

        <b-form-group label="Confirm Password:" label-for="confirm-password" label-cols-md="3">
          <b-form-input
            id="confirm-password"
            name="confirm-password"
            v-model="confirmPassword"
            type="password"
            required>
          </b-form-input>
        </b-form-group>

        <b-button type="submit" variant="primary" :disabled="loading">
          <span>Register</span>
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
  name: 'Register',
  data() {
    return {
      user: new User(),
      confirmPassword: null,
      message: '',
      loading: false,
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
      if (this.user.password !== this.confirmPassword) {
        this.message = { detail: 'Password fields must match' };
        return;
      }

      this.loading = true;

      this.$store.dispatch('auth/register', this.user).then(
        () => {
          this.$router.push('/login');
        },
        (error) => {
          console.error('Error registering');
          this.loading = false;
          this.message = (error.response && error.response.data)
              || error.message
              || error.toString();
          console.error(this.message);
        },
      );
    },
  },
};
</script>

<style lang="less" scoped>
  #register-container {
    margin-top: 25px;
  }
</style>
