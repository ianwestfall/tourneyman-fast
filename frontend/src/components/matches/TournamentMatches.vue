<template>
  <div>
    <div
      v-for="stage in tournament.stages.filter((stage) => stage.status > 0)"
      :key="stage.ordinal"
    >
      <h4>Stage {{ stage.ordinal + 1 }}</h4>
      <div v-for="pool in stage.pools" :key="pool.ordinal">
        <h5>Pool {{ pool.ordinal + 1 }}</h5>
        <!-- TODO Add in current standings by competitor component here -->
        <b-table :items="standings" :fields="fields" hover striped small dark>
        </b-table>
        <!-- TODO Componentize all of this -->
        <a v-b-toggle :href="`#pool-${pool.ordinal}-matches`" @click.prevent>Show matches</a>
        <b-collapse :id="`pool-${pool.ordinal}-matches`">
          <div v-for="match in pool.matches" :key="match.ordinal">
            <b-row style="margin-bottom: 10px" class="text-center">
              <b-col>
                <b-card :title="match.competitor1 | competitorDisplay">
                  <div v-if="!!match.competitor1.organization">
                      {{ match.competitor1.organization }}
                    </div>
                    <div v-if="!!match.competitor1.location">
                      {{ match.competitor1.location }}
                    </div>
                  <template #footer>
                    <div class="matchResult">
                      {{ match.competitor1Score }}
                    </div>
                  </template>
                </b-card>
              </b-col>
              <b-col cols="2" align-self="center" class="text-center">vs.</b-col>
              <b-col>
                <b-card :title="match.competitor2 | competitorDisplay">
                  <div v-if="!!match.competitor2.organization">
                    {{ match.competitor2.organization }}
                  </div>
                  <div v-if="!!match.competitor2.location">
                    {{ match.competitor2.location }}
                  </div>
                  <template #footer>
                    <div class="matchResult">
                      {{ match.competitor2Score }}
                    </div>
                  </template>
                </b-card>
              </b-col>
            </b-row>
          </div>
        </b-collapse>
        <hr />
      </div>
      <hr />
    </div>
  </div>
</template>

<script>
import Tournament from '@/models/tournament';

export default {
  name: 'TournamentMatches',
  props: {
    tournament: Tournament,
  },
  data() {
    return {
      fields: [
        {
          key: 'rank',
          sortable: true,
        }, {
          key: 'name',
          sortable: true,
        }, {
          key: 'wins',
          sortable: true,
        }, {
          key: 'losses',
          sortable: true,
        }, {
          key: 'ties',
          sortable: true,
        },
      ],
      standings: [
        {
          rank: 1,
          name: 'A',
          wins: 5,
          losses: 2,
          ties: 0,
        }, {
          rank: 2,
          name: 'C',
          wins: 5,
          losses: 2,
          ties: 0,
        }, {
          rank: 3,
          name: 'G',
          wins: 5,
          losses: 2,
          ties: 0,
        }, {
          rank: 4,
          name: 'D',
          wins: 5,
          losses: 2,
          ties: 0,
        }, {
          rank: 5,
          name: 'H',
          wins: 5,
          losses: 2,
          ties: 0,
        }, {
          rank: 6,
          name: 'F',
          wins: 5,
          losses: 2,
          ties: 0,
        },
      ],
    };
  },
};
</script>

<style scoped>
.matchResult {
  font-weight: bold;
}
</style>
