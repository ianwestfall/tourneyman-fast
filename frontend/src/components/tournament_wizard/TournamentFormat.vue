<template>
  <b-row>
    <b-col col xl="4" lg="8">
      <b-form @submit.prevent="onSubmit" @reset="onReset" v-if="show">
        <b-list-group>
          <b-list-group-item v-for="(stage, index) in tournament.stages" :key="index">
            <b-row>
              <b-col col cols="10">
                <stage-editor :stage="stage" />
              </b-col>
              <b-col col cols="2">
                <div class="float-right" v-if="index === tournament.stages.length - 1">
                  <b-button variant="danger" @click="removeStage">
                    <b-icon-x></b-icon-x>
                  </b-button>
                </div>
              </b-col>
            </b-row>
          </b-list-group-item>
          <b-list-group-item>
            <b-button @click="addStage" v-if="canAddAnotherStage">
              <b-icon-plus></b-icon-plus> Add another stage
            </b-button>
          </b-list-group-item>
        </b-list-group>
        <br />
        <b-button-group>
          <b-button type="reset" variant="danger">Reset</b-button>
          <b-button type="submit" variant="primary" :disabled="updating">
            <span v-if="!updating">Next</span>
            <b-spinner small label="Spinning" v-if="updating"></b-spinner>
          </b-button>
        </b-button-group>
      </b-form>
    </b-col>
  </b-row>
</template>

<script>
import Tournament from '@/models/tournament';
import Stage from '@/models/stage';
import StageEditor from '@/components/tournament_wizard/StageEditor.vue';
import StageService from '@/services/stage.service';

export default {
  components: { StageEditor },
  name: 'TournamentFormat',
  props: {
    tournament: Tournament,
  },
  data() {
    return {
      updating: false,
      show: true,
      stagesCreated: false,
    };
  },
  methods: {
    addStage() {
      this.tournament.stages.push(
        new Stage(null, this.tournament.stages.length, null, null, {}),
      );
    },
    removeStage() {
      this.tournament.stages.pop();
    },
    onReset() {
      this.tournament.stages = [new Stage(null, 0, null, null, {})];

      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    async onSubmit() {
      this.updating = true;
      // Make the call to create the stages on the tournament.
      try {
        const stages = await StageService.createStages(this.tournament, this.tournament.stages);

        this.$store.dispatch(
          'alerts/raiseInfo',
          `Successfully created ${stages.length} new stage(s) for tournament with id ${this.tournament.id}`,
        );

        this.stagesCreated = true;

        // Navigate to the next page
        this.$emit('next-page', stages);
      } catch (error) {
        this.$store.dispatch(
          'alerts/raiseError',
          `Failed to create new stage(s): ${error.toString()}`,
        );
      } finally {
        this.updating = false;
      }
    },
  },
  computed: {
    canAddAnotherStage() {
      if (!this.tournament || this.tournament.stages.length === 0) {
        return false;
      }

      const stageType = this.tournament.stages[this.tournament.stages.length - 1].type;
      return stageType === Stage.types[0].value;
    },
  },
  created() {
    if (this.tournament.stages.length === 0) {
      this.tournament.stages.push(new Stage(null, 0, null, null, {}));
    }
  },
};
</script>
