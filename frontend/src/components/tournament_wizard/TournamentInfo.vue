<template>
  <b-row>
    <b-col col xl="4" lg="8">
      <b-form @submit.prevent="onSubmit" @reset="onReset" v-if="show">
        <b-form-group
          label="Tournament name:"
          label-for="tournament-name"
          description="What will people call your tournament?"
        >
          <b-form-input id="tournament-name" v-model="tournamentName" required></b-form-input>
        </b-form-group>
        <b-form-group
          label="Organization:"
          label-for="tournament-org"
          description="Whose tournament is this?"
        >
          <b-form-input id="tournament-org" v-model="tournamentOrg"></b-form-input>
        </b-form-group>
        <b-form-group
          label="Start date:"
          label-for="tournament-start-date"
          description="When will the tournament start?"
        >
          <b-form-datepicker
            id="tournament-start-date"
            v-model="tournamentStartDate"
            required
            value-as-date
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
            v-model="tournamentPublic"
          ></b-form-checkbox>
        </b-form-group>
        <b-button-group>
          <b-button type="reset" variant="danger">Reset</b-button>
          <b-button type="submit" variant="primary" :disabled="updating">
            <span v-if="!updating">Next</span>
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
  data() {
    return {
      tournamentName: null,
      tournamentOrg: null,
      tournamentStartDate: null,
      tournamentPublic: false,
      show: true,
      message: '',
      updating: false,
      tournamentCreated: false,
    };
  },
  methods: {
    validate() {
      return this.tournamentName && this.tournamentStartDate;
    },
    async onSubmit() {
      if (this.tournamentCreated) {
        // Navigate to the next page without further action if the tournament has already been
        // created, like when a user navigates back to this page from a later step.
        // TODO: Perform an update if anything has changed.
        this.$emit('next-page');
        return;
      }

      // Lock the button so users can't click it twice on accident
      this.updating = true;

      if (this.validate()) {
        // Create a new tournament
        try {
          const tournamentModel = new Tournament(
            null,
            this.tournamentName,
            this.tournamentOrg,
            this.tournamentStartDate,
            this.tournamentPublic,
            null,
            null,
          );
          const tournament = await TournamentService.createTournament(tournamentModel);
          this.$store.dispatch(
            'alerts/raiseInfo',
            `Successfully created a new tournament with id ${tournament.id}!`,
          );

          this.tournamentCreated = true;

          // Navigate to the next page
          this.$emit('next-page', tournament);
        } catch (error) {
          this.$store.dispatch(
            'alerts/raiseError',
            `Failed to create a new tournament: ${error.toString()}`,
          );
        } finally {
          this.updating = false;
        }
      } else {
        this.message = 'Tournament name and start date are required';
        this.updating = false;
      }
    },
    onReset() {
      this.tournamentName = null;
      this.tournamentOrg = null;
      this.tournamentStartDate = null;
      this.tournamentPublic = false;
      this.message = '';

      // This gets rid of the browser validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
};
</script>
