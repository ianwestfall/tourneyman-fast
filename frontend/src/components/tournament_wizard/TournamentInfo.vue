<template>
  <b-row>
    <b-col col xl="4" lg="8">
      <b-form @submit.prevent="onSubmit" @reset="onReset" v-if="show">
        <b-form-group
          label="Tournament name:"
          label-for="tournament-name"
          description="What will people call your tournament?"
        >
          <b-form-input
            id="tournament-name"
            v-model="tournament.name"
            required
            :disabled="disabled">
          </b-form-input>
        </b-form-group>
        <b-form-group
          label="Organization:"
          label-for="tournament-org"
          description="Whose tournament is this?"
        >
          <b-form-input
            id="tournament-org"
            v-model="tournament.organization"
            :disabled="disabled">
          </b-form-input>
        </b-form-group>
        <b-form-group
          label="Start date:"
          label-for="tournament-start-date"
          description="When will the tournament start?"
        >
          <b-form-datepicker
            id="tournament-start-date"
            v-model="tournament.startDate"
            required
            value-as-date
            :disabled="disabled"
          >
          </b-form-datepicker>
        </b-form-group>
        <b-form-group
          label="Public:"
          label-for="tournament-public"
          description="Should anyone be able to view this tournament, or just you?"
        >
          <b-form-checkbox
            id="tournament-public"
            v-model="tournament.public"
            :disabled="disabled"
          ></b-form-checkbox>
        </b-form-group>
        <b-button-group v-if="!disabled">
          <b-button type="reset" variant="danger" v-if="!tournamentCreated">Reset</b-button>
          <b-button type="submit" variant="primary" :disabled="updating">
            <span v-if="!updating">{{ tournamentCreated ? 'Update': 'Next' }}</span>
            <b-spinner small label="Spinning" v-if="updating"></b-spinner>
          </b-button>
        </b-button-group>
        <div v-if="message" class="text-danger">{{ message }}</div>
      </b-form>
    </b-col>
  </b-row>
</template>

<script>
import Tournament from '@/models/tournament';
import TournamentService from '@/services/tournament.service';

export default {
  name: 'TournamentInfo',
  props: {
    tournament: {
      type: Tournament,
      default: () => new Tournament(),
    },
    editable: {
      type: Boolean,
      default: () => true,
    },
  },
  data() {
    return {
      show: true,
      message: '',
      updating: false,
    };
  },
  methods: {
    validate() {
      return this.tournament.name && this.tournament.startDate;
    },
    async onSubmit() {
      // Lock the button so users can't click it twice on accident
      this.updating = true;

      // Make sure the data is valid
      if (!this.validate()) {
        this.message = 'Tournament name and start date are required';
      } else if (this.tournamentCreated) {
        // Update an existing tournament
        try {
          const tournament = await TournamentService.updateTournament(this.tournament);
          this.$store.dispatch(
            'alerts/raiseInfo',
            `Successfully updated tournament with id ${tournament.id}!`,
          );
          this.$emit('updated', tournament);
        } catch (error) {
          this.$store.dispatch(
            'alerts/raiseError',
            `Failed to update tournament ${this.tournament.id}: ${error.toString()}`,
          );
        }
      } else {
        // Create a new tournament
        try {
          const tournament = await TournamentService.createTournament(this.tournament);
          this.$store.dispatch(
            'alerts/raiseInfo',
            `Successfully created a new tournament with id ${tournament.id}!`,
          );

          // Navigate to the next page
          this.$emit('updated', tournament);
        } catch (error) {
          this.$store.dispatch(
            'alerts/raiseError',
            `Failed to create a new tournament: ${error.toString()}`,
          );
        }
      }

      this.updating = false;
    },
    onReset() {
      this.tournament.name = undefined;
      this.tournament.organization = undefined;
      this.tournament.startDate = undefined;
      this.tournament.public = false;

      this.message = '';

      // This gets rid of the browser validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
  computed: {
    tournamentCreated() {
      return !!this.tournament.id;
    },
    disabled() {
      return !this.editable || this.tournament.status > 1;
    },
  },
};
</script>
