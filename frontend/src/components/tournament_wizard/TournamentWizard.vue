<template>
  <b-card no-body>
    <b-tabs pills card vertical>
      <b-tab active title="Basic Info">
        <tournament-info />
      </b-tab>
      <b-tab disabled title="Tournament Format"></b-tab>
      <b-tab disabled title="Venue Info"></b-tab>
      <b-tab disabled title="Competitors"></b-tab>
    </b-tabs>
  </b-card>
</template>

<script>
import TournamentInfo from '@/components/tournament_wizard/TournamentInfo.vue';

export default {
  components: { TournamentInfo },
  name: 'TournamentWizard',
  data() {
    return {};
  },
  props: {
    tournamentId: Number,
  },
};
</script>

<style lang="less" scoped>

</style>
