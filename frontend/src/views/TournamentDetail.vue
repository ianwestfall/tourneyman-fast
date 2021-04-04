<template>
  <b-card no-body>
    <b-tabs card>
      <b-tab title="Tournament Info">
        <tournament-info :tournament="tournament"></tournament-info>
      </b-tab>
      <b-tab title="Format">
        <tournament-format :tournament="tournament"></tournament-format>
      </b-tab>
      <b-tab title="Competitors">
        <tournament-competitors :tournament="tournament"></tournament-competitors>
      </b-tab>
    </b-tabs>
  </b-card>
</template>

<script>
import Tournament from '@/models/tournament';
import TournamentService from '@/services/tournament.service';
import TournamentInfo from '@/components/tournament_wizard/TournamentInfo.vue';
import TournamentFormat from '@/components/tournament_wizard/TournamentFormat.vue';
import TournamentCompetitors from '@/components/tournament_wizard/TournamentCompetitors.vue';

export default {
  name: 'TournamentDetail',
  components: { TournamentInfo, TournamentFormat, TournamentCompetitors },
  props: {
    id: Number,
  },
  data() {
    return {
      tournament: new Tournament(),
    };
  },
  async created() {
    this.tournament = await TournamentService.getTournament(this.id);
  },
};
</script>
