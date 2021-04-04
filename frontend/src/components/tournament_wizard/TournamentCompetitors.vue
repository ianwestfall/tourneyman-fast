<template>
  <b-row>
    <b-col col>
      <b-form @submit.prevent="onSubmit" @reset="onReset" v-if="show">
        <b-table id="competitors"
          hover
          striped
          small
          sticky-header="500px"
          dark
          :items="tournament.competitors"
          :fields="fields"
        >
          <template #head(index)>
            <span></span>
          </template>
          <template #cell(index)="data">
            {{ data.index + 1 }}
          </template>
          <template #cell(firstName)="data">
            <b-form-input v-model="data.item.firstName"></b-form-input>
          </template>
          <template #cell(lastName)="data">
            <b-form-input v-model="data.item.lastName"></b-form-input>
          </template>
          <template #cell(organization)="data">
            <b-form-input v-model="data.item.organization"></b-form-input>
          </template>
          <template #cell(location)="data">
            <b-form-input v-model="data.item.location"></b-form-input>
          </template>
          <template #cell(remove)="data">
            <b-button
              variant="danger"
              @click="removeCompetitor(data.index)"
            >
              <b-icon-x></b-icon-x>
            </b-button>
          </template>
        </b-table>
        <b-button-group>
          <b-button @click="addCompetitor">
            <b-icon-plus></b-icon-plus> Add another competitor
          </b-button>
          <b-button variant="success" v-b-modal.helpModal>
            <b-icon-question-circle-fill></b-icon-question-circle-fill>
          </b-button>
        </b-button-group>
        <br />
        <br />
        <b-button-group>
          <b-button type="reset" variant="danger" v-if="!competitorsCreated">Reset</b-button>
          <b-button type="submit" variant="primary" :disabled="updating">
            <span v-if="!updating">{{ competitorsCreated ? 'Update' : 'Finish' }}</span>
            <b-spinner small label="Spinning" v-if="updating"></b-spinner>
          </b-button>
        </b-button-group>
      </b-form>
      <b-modal id="helpModal" title="Help" ok-only>
        <p>
          Competitors generally fall into two categories: individual people and teams.
        </p>
        <p>
          For individual people, at least a last name is required.
          All other fields are optional, but will add information
          when the competitor is displayed on screen.
        </p>
        <p>
          For teams, just an organization name is required, and name data will be ignored.
        </p>
      </b-modal>
    </b-col>
  </b-row>
</template>

<script>
import Tournament from '@/models/tournament';
import Competitor from '@/models/competitor';
import CompetitorService from '@/services/competitor.service';

export default {
  name: 'TournamentCompetitors',
  props: {
    tournament: Tournament,
  },
  data() {
    return {
      updating: false,
      show: true,
      fields: ['index', 'firstName', 'lastName', 'organization', 'location', 'remove'],
    };
  },
  methods: {
    async onSubmit() {
      this.updating = true;
      try {
        const competitors = await CompetitorService.createCompetitors(
          this.tournament,
          this.tournament.competitors,
        );

        // Navigate to the next page
        this.$emit('next-page', competitors);
      } catch (error) {
        this.$store.dispatch(
          'alerts/raiseError',
          `Failed to create new competitor(s): ${error.toString()}`,
        );
      } finally {
        this.updating = false;
      }
    },
    onReset() {
      this.tournament.competitors = [new Competitor()];

      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    addCompetitor() {
      this.tournament.competitors.push(new Competitor());

      this.$nextTick(() => {
        // Give Vue a chance to create the new table row, then scroll to it.
        const lastRow = document.getElementById('competitors').querySelector('tbody tr:last-child');
        lastRow.scrollIntoView();
      });
    },
    removeCompetitor(index) {
      this.tournament.competitors.splice(index, 1);
    },
  },
  computed: {
    competitorsCreated() {
      return this.tournament
        && this.tournament.competitors
        && this.tournament.competitors.some((competitor) => !!competitor.id);
    },
  },
};
</script>