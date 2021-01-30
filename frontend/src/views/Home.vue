<template>
  <div class="home">
    <div>
      <b-card no-body>
        <b-tabs card content-class="mt-3">
          <b-tab title="All Tournaments" active>
            <tournament-table :isFilteredByUser="false"/>
          </b-tab>
          <b-tab title="My Tournaments" v-if="$store.getters['auth/loggedIn']">
            <tournament-table :isFilteredByUser="true"/>
          </b-tab>
        </b-tabs>
      </b-card>
    </div>
  </div>
</template>

<script>
import TournamentTable from '../components/TournamentTable.vue';

export default {
  components: { TournamentTable },
  name: 'Home',
};
</script>

<style lang="less" scoped>
</style>
