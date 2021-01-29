<template>
  <div class="home">
    <h1>Welcome!</h1>
    <div>
      <div id="myTournaments" class="tournament-list" v-if="$store.getters['auth/loggedIn']">
        <h3>My Tournaments</h3>
        <b-table
          striped
          hover
          fixed
          :items="privateTournaments"
          :fields="fields"></b-table>
      </div>
      <div id="publicTournaments" class="tournament-list">
        <h3>Public Tournaments</h3>
        <b-table
          striped
          hover
          fixed
          :items="publicTournaments"
          :fields="fields"></b-table>
      </div>
    </div>
  </div>
</template>

<script>
import TournamentService from '@/services/tournament.service';

export default {
  name: 'Home',
  data() {
    return {
      tournaments: [],
      fields: [
        {
          key: 'name',
        }, {
          key: 'organization',
        }, {
          key: 'startDate',
          formatter: (d) => d.toDateString(),
        }, {
          key: 'status',
        },
      ],
    };
  },
  computed: {
    privateTournaments() {
      const authenticatedUser = this.$store.getters['auth/authenticatedUser'];
      return this.tournaments.filter(
        (tournament) => tournament.owner.getUsername() === authenticatedUser.getUsername(),
      );
    },
    publicTournaments() {
      const authenticatedUser = this.$store.getters['auth/authenticatedUser'];
      return this.tournaments.filter(
        (tournament) => tournament.owner.getUsername() !== authenticatedUser.getUsername(),
      );
    },
  },
  async created() {
    this.tournaments = await TournamentService.getTournaments();
  },
};
</script>

<style lang="less" scoped>
.tournament-list {
  padding: 10px;
}
</style>
