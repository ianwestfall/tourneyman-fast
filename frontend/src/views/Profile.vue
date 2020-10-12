<template>
  <div>
    <h1>{{ profile.email }}'s Profile</h1>
    <h2>{{ profile.id }}</h2>
    <h2>{{ profile.is_active }}</h2>
  </div>
</template>

<script>
import UserService from '../services/user-service';

export default {
  name: 'Profile',
  data() {
    return {
      profile: {},
    };
  },
  async created() {
    this.profile = await UserService.getProfile();
  },
};
</script>

<style lang="less" scoped>

</style>
