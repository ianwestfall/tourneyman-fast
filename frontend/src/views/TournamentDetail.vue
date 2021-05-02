<template>
  <div>
    <b-card :title="`Tournament Status: ${humanReadableStatus}`">
      <div>
        <b-button
          v-if="tournament.status === 1 && editable"
          variant="primary"
          @click="startTournament"
        >
          Start Tournament
        </b-button>
      </div>
    </b-card>
    <b-card no-body>
      <b-tabs card>
        <b-tab title="Tournament Info">
          <tournament-info
            :tournament="tournament"
            @updated="updateBasicInfo"
            :editable="editable"
          ></tournament-info>
        </b-tab>
        <b-tab title="Format">
          <tournament-format
            :tournament="tournament"
            @updated="updateFormat"
            :editable="editable"
          ></tournament-format>
        </b-tab>
        <b-tab title="Competitors">
          <tournament-competitors
            :tournament="tournament"
            @updated="updateCompetitors"
            :editable="editable"
          ></tournament-competitors>
        </b-tab>
        <b-tab title="Matches" v-if="tournament.status > 1">
          <tournament-matches :tournament="tournament"></tournament-matches>
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import Tournament from '@/models/tournament';
import TournamentService from '@/services/tournament.service';
import TournamentInfo from '@/components/tournament_wizard/TournamentInfo.vue';
import TournamentFormat from '@/components/tournament_wizard/TournamentFormat.vue';
import TournamentCompetitors from '@/components/tournament_wizard/TournamentCompetitors.vue';
import TournamentMatches from '@/components/matches/TournamentMatches.vue';
import tournamentStatusFilter from '@/filters/tournamentStatus.filter';

export default {
  name: 'TournamentDetail',
  components: {
    TournamentInfo,
    TournamentFormat,
    TournamentCompetitors,
    TournamentMatches,
  },
  props: {
    id: Number,
  },
  data() {
    return {
      tournament: new Tournament(),
    };
  },
  methods: {
    updateBasicInfo(tournament) {
      this.tournament = tournament;
    },
    updateFormat(stages) {
      this.tournament.stages = stages;
    },
    updateCompetitors(competitors) {
      this.tournament.competitors = competitors;
    },
    async startTournament() {
      this.tournament = await TournamentService.updateTournamentStatus(this.tournament, 2);
    },
  },
  async created() {
    this.tournament = await TournamentService.getTournament(this.id);
  },
  computed: {
    editable() {
      const user = this.$store.getters['auth/authenticatedUser'];
      return this.tournament
        && user
        && this.tournament.owner
        && this.tournament.owner.email === user.email;
    },
    humanReadableStatus() {
      return tournamentStatusFilter(this.tournament.status);
    },
  },
};
</script>
