<template>
  <div v-if="subjects">
    <h1 class="text-center">Wyniki (do tej pory)</h1>
    <div class="row justify-between">
      <div class="col-2 column">
        <div class="text-center subject">{{ firstChallenger }}</div>
        <div class="text-center score" :class="getWinnerLoser(1)">{{ firstChallengerScore }} głosów!</div>
      </div>
      <div class="col-2 column">
        <div class="text-center subject">{{ secondChallenger }}</div>
        <div class="text-center score" :class="getWinnerLoser(2)">{{ secondChallengerScore }} głosów!</div>
      </div>
    </div>
      <div
          v-for="(sub_data, sub_name) in subjects"
          :key="sub_name"
          class="row q-pa-md justify-between items-center"
      >
        <img
            class="photo col-2"
            :class="chosen.includes(sub_data[firstChallenger].id) ? 'highlighted' : ''"
            :src="sub_data[firstChallenger].photo"
        >
        <div class="column col justify-center">
        <div class="text-center subject">{{ sub_name }}</div>
          <div class="q-mx-xl row">
            <div class="results-left" :style="calculateWidth(sub_data, 1)">
              <div class="text-center result-val">{{ sub_data[firstChallenger].votes}}</div>
            </div>
            <div class="results-right" :style="calculateWidth(sub_data, 2)">
              <div class="text-center result-val">{{ sub_data[secondChallenger].votes }}</div>
            </div>
          </div>
        </div>
        <img
            class="photo col-2"
            :class="chosen.includes(sub_data[secondChallenger].id) ? 'highlighted' : ''"
            :src="sub_data[secondChallenger].photo"
        >
        </div>
    </div>
</template>

<script>
import {Cookies} from 'quasar';
import {api} from 'boot/axios';

export default {
  name: 'VotePage',
  data() {
    return {
      challengeId: Cookies.get('challenge'),
      token: Cookies.get('auth_token'),
      chosen: null,
      subjects: null,
      firstChallenger: null,
      secondChallenger: null,
      firstChallengerScore: 0,
      secondChallengerScore: 0,
    };
  },
  mounted() {
    this.getResults();
  },
  methods: {
    getResults() {
      api
          .get(
              `results/?challenge_id=${this.challengeId}`,
              {
                headers: {Authorization: `Token ${this.token}`},
              },
          )
          .then((response) => {
            this.chosen = response.data.chosen;
            this.subjects = response.data.subjects;
            this.firstChallenger = response.data.owners[0].id;
            this.secondChallenger = response.data.owners[1].id;
            this.firstChallengerScore = response.data.owners[0].score;
            this.secondChallengerScore = response.data.owners[1].score;
          })
          .catch((response) => {
            console.error(response);
          });
    },
    calculateWidth(subData, challengerId) {
      let challenger = subData[this.firstChallenger];
      let opponent = subData[this.secondChallenger];
      if (challengerId === 2) {
        const temp = challenger;
        challenger = opponent;
        opponent = temp;
      }
      const votesMy = challenger.votes;
      const votesThem = opponent.votes;
      const width = votesMy / (votesMy + votesThem) * 100;
      return `width: ${width}%`;
    },
    getWinnerLoser(challengerId) {
      if (challengerId === 1) {
        return this.firstChallengerScore > this.secondChallengerScore ? 'winner' : 'loser';
      } else if (challengerId === 2) {
        return this.secondChallengerScore > this.firstChallengerScore ? 'winner' : 'loser';
      }
    },
  },
  computed: {
    highlightSelected(obj) {
      console.log(obj);
      return '';
    },
  },
};
</script>

<style scoped lang="scss">

.photo {
  max-width:100%;
  height: auto;
}

.subject {
  font-size: 3em;
}

.result-val {
  font-size: 35px;
}

.highlighted {
  border: 5px solid $primary-dark;
}

.results-left {
  width: 60%;
  height: 50px;
  background-color: $accent-dark;
}

.results-right {
  width: 40%;
  height: 50px;
  background-color: $secondary;
}

.score {
  font-size: 3em;
}

.winner {
  color: $positive;
}

.loser {
  color: $negative;
}

</style>
