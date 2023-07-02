<template>
  <div v-if="stats">
    <h1 class="text-center">Wyniki (do tej pory)</h1>
    <div class="row justify-between">
      <div class="col-2 row">
        <div class="text-center subject">Ania i Jacek</div>
      </div>
      <div class="text-center subject col-2 row">Marta i Kasia</div>
<!--      <div class="text-center subject col-2">{{ stats.player1 }}</div>-->
<!--      <div class="text-center subject col-2">{{ stats.player2 }}</div>-->
    </div>
      <div
          v-for="stat in stats"
          :key="stat.chosen_entry"
          class="column q-pa-md"
      >
        <div class="text-center subject">{{ stat.subject_name }}</div>
        <div class="row justify-between items-center">
          <img
              class="photo col-2"
              :class="stat.entries[0].id === stat.chosen_entry ? 'highlighted' : ''"
              :src="stat.entries[0].photo"
          >
          <div class="col q-mx-xl row">
            <div class="results-left"><div class="text-center result-val">3</div></div>
            <div class="results-right"><div class="text-center result-val">2</div></div>
          </div>
          <img
              class="photo col-2"
              :class="stat.entries[1].id === stat.chosen_entry ? 'highlighted' : ''"
              :src="stat.entries[1].photo"
          >
        </div>
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
      token: Cookies.get('auth_token'),
      stats: null,
    };
  },
  mounted() {
    this.getResults();
  },
  methods: {
    getResults() {
      api
          .get(
              `results/`,
              {
                headers: {Authorization: `Token ${this.token}`},
              },
          )
          .then((response) => {
            console.log(response);
            this.stats = response.data;
            console.log(this.stats[0]);
          })
          .catch((response) => {
            console.error(response);
          });
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
  max-width: 200px;
  object-fit: cover;
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

</style>
