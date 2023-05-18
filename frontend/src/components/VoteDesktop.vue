<template>
  <h1 class="text-center q-mb-sm">Głosuj na ładniejsze zdjęcie!</h1>
  <p class="text-center">
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
</template>

<script>
// TODO: enhance photo

export default {
  name: 'VoteDesktop',
  props: {
    entries: {
      type: Array,
    },
    subject: {
      type: Object,
    },
  },
  emits: ['vote'],
  mounted() {
    // TODO: log errors
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
      this.$emit('vote', entryId);
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
