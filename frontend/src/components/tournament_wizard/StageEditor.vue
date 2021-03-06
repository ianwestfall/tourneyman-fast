<template>
  <div>
    <span>Stage #{{ stage.ordinal + 1 }}</span>
    <b-form-group
      description="What type of stage is this?"
    >
      <b-form-select id="stage-type" v-model="stage.type" :options="stageTypes" required>
      </b-form-select>
    </b-form-group>
    <div v-if="stage.type === 0">
      <!-- Put pool-type configuration here -->
      <b-form-group
        label="Minimum pool size:"
        description="What's the smallest pool size? All pools will be this size or 1 larger."
      >
        <b-form-input id="minimum-pool-size" type="number" required></b-form-input>
      </b-form-group>
    </div>
    <div v-if="stage.type === 1 || stage.type === 2">
      <!-- Put bracket-type configuration here -->
      <b-form-group
        label="Seeding type:"
        description="Should the bracket take seed values into account or be randomized?"
      >
        <b-form-radio-group required>
          <b-form-radio value="1">Seeded</b-form-radio>
          <b-form-radio value="0">Randomized</b-form-radio>
        </b-form-radio-group>
      </b-form-group>
    </div>
  </div>
</template>

<script>
import Stage from '@/models/stage';

export default {
  name: 'StageEditor',
  props: {
    stage: Stage,
  },
  data() {
    return {
      stageTypes: [{ value: null, text: 'Select a stage type' }].concat(Stage.types),
    };
  },
};
</script>
