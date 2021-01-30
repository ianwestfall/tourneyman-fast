<template>
  <div class="home">
    <div>
      <b-card no-body>
        <b-tabs card content-class="mt-3">
          <b-tab title="All Tournaments">
            <tournament-table :isFilteredByUser="false"/>
          </b-tab>
          <b-tab lazy title="My Tournaments" v-if="$store.getters['auth/loggedIn']">
            <tournament-table :isFilteredByUser="true"/>
          </b-tab>
          <b-tab lazy active title="New Tournament" v-if="$store.getters['auth/loggedIn']">
            <tournament-wizard />
          </b-tab>
        </b-tabs>
      </b-card>
    </div>
  </div>
</template>

<script>
import TournamentTable from '@/components/TournamentTable.vue';
import TournamentWizard from '@/components/tournament_wizard/TournamentWizard.vue';

export default {
  components: { TournamentTable, TournamentWizard },
  name: 'Home',
};
</script>

<style lang="less" scoped>
</style>
