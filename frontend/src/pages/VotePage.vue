<template>
  <div v-if="entries">
    <h1 class="text-center q-mb-sm">Głosuj na ładniejsze zdjęcie!</h1>
    <p v-if="isMobile" class="text-center">
      (przesuń prawo-lewo żeby zobaczyć kandydatów, dotknij żeby zagłosować)
    </p>
    <p v-else class="text-center">
      (kliknij na obrazek albo klawisz lewo/prawo na klawiaturze)

    </p>
    <h2 class="text-center"> Temat: {{ subject.name }}</h2>
    <div class="row justify-center">
      <div
          class="col-5 text-center"
          v-for="entry in entries"
          :key="entry.id"
          @click="registerVote(entry.id)"
      >
        <img class="candidate-photo" :src="entry.photo">
      </div>
    </div>
  </div>
  <div v-else class="row justify-center">
    Nie masz już żadnych zdjęć do oceny w tym challenge'u ;)
  </div>
</template>

<script>
import {Cookies} from 'quasar';
import {api} from 'boot/axios';
// TODO: enhance photo

export default {
  name: 'VotePage',
  data() {
    return {
      isMobile: false,
      subject: {name: null, id: null},
      entries: null,
      challengeId: Cookies.get('challenge'),
      token: Cookies.get('auth_token'),
    };
  },
  mounted() {
    // TODO: log errors
    this.getPicks();
    window.addEventListener('keyup', this.parseKeyboardVote);
  },
  methods: {
    parseKeyboardVote(evt) {
      if (evt.key === 'ArrowLeft') {
        this.registerVote(this.entries[0].id);
      }
      if (evt.key === 'ArrowRight') {
        this.registerVote(this.entries[1].id);
      }
    },
    registerVote(entryId) {
      api
          .post(
              'vote/',
              {
                subject_id: this.subject.id,
                entry_id: entryId,
              },
              {
                headers: {Authorization: `Token ${this.token}`},
              },
          )
          .then(this.getPicks)
          .catch((response) => console.log(response))
      ;
    },
    getPicks() {
      api
          .get(
              `available_picks/?challenge_id=${this.challengeId}`,
              {
                headers: {Authorization: `Token ${this.token}`},
              },
          )
          .then((response) => {
            console.log(response);
            this.entries = response.data.entries;
            this.subject = {name: response.data.name, id: response.data.id};
          })
          .catch(
              (response) => {
                this.entries = null;
                console.error(response);
              });
    },
  },
};
</script>

<style scoped>
.candidate-photo {
  max-width: 100%;
  height: 500px;
}
</style>
