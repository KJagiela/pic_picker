<template>
  <div v-if="entries">
    <h1 class="text-center q-mb-sm">Głosuj na ładniejsze zdjęcie!</h1>
    <p v-if="isMobile" class="text-center">
      (przesuń prawo-lewo żeby zobaczyć kandydatów, dotknij żeby zagłosować)
    </p>
    <p v-else class="text-center">
      (kliknij na obrazek, albo klawisz prawo/lewo na klawiaturze)

    </p>
    <h2 class="text-center"> Temat: {{ subject }}</h2>
    <div class="row justify-around">
      <div
          class="col-5"
          v-for="entry in entries"
          :key="entry.id"
          @click="registerVote(entry.id)"
      >
        <img class="candidate-photo" :src="entry.photo">
      </div>
    </div>
  </div>
</template>

<script>
import {api} from 'boot/axios';

export default {
  name: 'VotePage',
  data() {
    return {
      isMobile: false,
      subject: null,
      entries: [],
    };
  },
  mounted() {
    // TODO: log errors
    api
        .get(
            'available_picks/' +
            '?challenge_id=3ab58738-02bd-4dd0-9df3-79e75a1cdb9c',
            {
              headers:
                  {
                    Authorization:
                        'Token 1da510a6e5b308a896e9a2919f5b377600341ae3',
                  },
            },
        )
        .then((response) => {
          console.log(response);
          this.entries = response.data.entries;
          this.subject = response.data.name;
        })
        .catch((response) => console.error(response));
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
      console.log(`voting for ${entryId}`);
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
