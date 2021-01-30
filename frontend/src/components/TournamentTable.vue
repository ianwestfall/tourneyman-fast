<template>
  <div>
    <b-pagination
      v-model="currentPage"
      :per-page="perPage"
      :total-rows="total"
      :aria-controls="id"
    ></b-pagination>
    <b-table
      :id="id"
      striped
      hover
      dark
      responsive
      :items="provider"
      :fields="fields"
      :per-page="perPage"
      :current-page="currentPage"></b-table>
  </div>
</template>

<script>
import TournamentService from '@/services/tournament.service';
import Tournament from '@/models/tournament';

export default {
  name: 'TournamentTable',
  data() {
    return {
      id: null,
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
          formatter: (s) => Tournament.convertStatusCode(s),
        },
      ],
      perPage: 20,
      currentPage: 1,
      total: 0,
    };
  },
  props: {
    isFilteredByUser: Boolean,
  },
  methods: {
    async provider(ctx) {
      try {
        const response = await TournamentService.getTournaments(
          this.isFilteredByUser, ctx.perPage, ctx.currentPage,
        );
        this.total = response.total;
        return response.items;
      } catch (error) {
        this.$store.dispatch(
          'alerts/raiseError',
          `Failed to load tournaments: ${error.toString()}`,
        );
        return [];
      }
    },
  },
  mounted() {
    this.id = `tournament-table-${this._uid}`;
  },
};
</script>

<style scoped>

</style>
