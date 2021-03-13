<template>
  <b-card no-body>
    <b-tabs pills card vertical v-model="currentTabIndex" @activate-tab="checkActiveTab">
      <b-tab title="Basic Info">
        <tournament-info @next-page="updateBasicInfo"/>
      </b-tab>
      <b-tab title="Tournament Format">
        <tournament-format :tournament="tournament" @next-page="updateFormat"/>
      </b-tab>
      <b-tab title="Competitors">
        <tournament-competitors :tournament="tournament" @next-page="updateCompetitors" />
      </b-tab>
    </b-tabs>
  </b-card>
</template>

<script>
import Tournament from '@/models/tournament';
import Stage from '@/models/stage';
import TournamentInfo from '@/components/tournament_wizard/TournamentInfo.vue';
import TournamentFormat from '@/components/tournament_wizard/TournamentFormat.vue';
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
      this.nextPage();
    },
    updateCompetitors() {},
    isTabActive(tabIndex) {
      return tabIndex === this.currentTabIndex;
    },
  },
};
</script>
