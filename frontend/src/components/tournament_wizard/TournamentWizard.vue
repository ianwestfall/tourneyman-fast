<template>
  <b-card no-body>
    <b-tabs pills card vertical v-model="currentTabIndex" @activate-tab="checkActiveTab">
      <b-tab title="Basic Info">
        <tournament-info :tournament="tournament" @updated="updateBasicInfo"/>
      </b-tab>
      <b-tab title="Tournament Format">
        <tournament-format :tournament="tournament" @updated="updateFormat"/>
      </b-tab>
      <b-tab title="Competitors">
        <tournament-competitors :tournament="tournament" @updated="updateCompetitors" />
      </b-tab>
    </b-tabs>
  </b-card>
</template>

<script>
import Tournament from '@/models/tournament';
import Stage from '@/models/stage';
import Competitor from '@/models/competitor';
import TournamentInfo from '@/components/tournament_wizard/TournamentInfo.vue';
import TournamentFormat from '@/components/tournament_wizard/TournamentFormat.vue';
import TournamentService from '@/services/tournament.service';
import TournamentCompetitors from './TournamentCompetitors.vue';

export default {
  components: { TournamentInfo, TournamentFormat, TournamentCompetitors },
  name: 'TournamentWizard',
  data() {
    return {
      currentTabIndex: 0,
      tabsCompleted: 0,
      tournament: new Tournament(null, null, null, null, null, null, null, []),
    };
  },
  methods: {
    checkActiveTab(newTabIndex, prevTabIndex, bvEvent) {
      // Don't let the user navigate ahead manually
      if (newTabIndex > this.tabsCompleted) {
        bvEvent.preventDefault();
      }
    },
    nextPage() {
      if (this.currentTabIndex < 2) {
        // Increment the current tab index if it isn't maxed out yet
        this.currentTabIndex += 1;
        this.tabsCompleted += 1;
      }
    },
    updateBasicInfo(tournament) {
      // Tournament is a tournament model object returned by the POST handler.
      this.tournament = tournament;
      if (this.tournament.stages.length === 0) {
        this.tournament.stages.push(new Stage(null, 0, null, null, {}));
      }
      this.nextPage();
    },
    updateFormat(stages) {
      // stages is a list of stage model objects returned by the POST handler.
      this.tournament.stages = stages;
      if (this.tournament.competitors.length === 0) {
        this.tournament.competitors.push(new Competitor());
      }
      this.nextPage();
    },
    async updateCompetitors(competitors) {
      this.tournament.competitors = competitors;

      // Move the tournament out of pending and into ready
      this.tournament = await TournamentService.updateTournamentStatus(this.tournament, 1);
      this.$router.push({ name: 'Tournament Detail', params: { id: this.tournament.id } });
    },
    isTabActive(tabIndex) {
      return tabIndex === this.currentTabIndex;
    },
  },
};
</script>
