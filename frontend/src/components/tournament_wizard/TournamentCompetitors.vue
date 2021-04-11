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
            <b-form-input v-model="data.item.firstName" :disabled="disabled"></b-form-input>
          </template>
          <template #cell(lastName)="data">
            <b-form-input v-model="data.item.lastName" :disabled="disabled"></b-form-input>
          </template>
          <template #cell(organization)="data">
            <b-form-input v-model="data.item.organization" :disabled="disabled"></b-form-input>
          </template>
          <template #cell(location)="data">
            <b-form-input v-model="data.item.location" :disabled="disabled"></b-form-input>
          </template>
          <template #cell(remove)="data" v-if="!disabled">
            <b-button
              variant="danger"
              @click="removeCompetitor(data.index)"
            >
              <b-icon-x></b-icon-x>
            </b-button>
          </template>
        </b-table>
        <div v-if="!disabled">
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
        </div>
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
    editable: {
      type: Boolean,
      default: () => true,
    },
  },
  data() {
    return {
      updating: false,
      show: true,
    };
  },
  methods: {
    async onSubmit() {
      this.updating = true;

      if (this.competitorsCreated) {
        // Update existing competitors, create new ones, delete missing ones.
        try {
          const competitors = await CompetitorService.updateCompetitors(
            this.tournament,
            this.tournament.competitors,
          );

          this.$store.dispatch(
            'alerts/raiseInfo',
            `Successfully updated competitors for tournament with id ${this.tournament.id}`,
          );

          this.$emit('updated', competitors);
        } catch (error) {
          this.$store.dispatch(
            `Failed to update competitors for tournament with id ${this.tournament.id}`,
          );
        }
      } else {
        try {
          const competitors = await CompetitorService.createCompetitors(
            this.tournament,
            this.tournament.competitors,
          );

          this.$store.dispatch(
            'alerts/raiseInfo',
            `Successfully created ${competitors.length} new competitor(s) for tournament with id ${this.tournament.id}`,
          );

          // Navigate to the next page
          this.$emit('updated', competitors);
        } catch (error) {
          this.$store.dispatch(
            'alerts/raiseError',
            `Failed to create new competitor(s): ${error.toString()}`,
          );
        }
      }

      this.updating = false;
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
    disabled() {
      return !this.editable || this.tournament.status > 1;
    },
    fields() {
      const fields = ['index', 'firstName', 'lastName', 'organization', 'location'];
      if (!this.disabled) {
        fields.push('remove');
      }
      return fields;
    },
  },
};
</script>
