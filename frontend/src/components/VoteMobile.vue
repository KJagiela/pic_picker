<template>
  <h1 class="text-center q-mb-sm">Głosuj na ładniejsze zdjęcie!</h1>
  <p class="text-center">
    (przesuń prawo-lewo żeby zobaczyć kandydatów, dotknij dwukrotnie żeby zagłosować)
  </p>
  <h2 class="text-center q-my-sm"> {{ subject.name }}</h2>
  <q-carousel
      v-model="slide"
      animated
      class="rounded-borders"
      swipeable
  >
    <q-carousel-slide
        :name="entry.id"
        v-for="entry in entries"
        :key="entry.id"
        :img-src="entry.photo"
        @click="registerTap"
        class="photo-slide"
    />
  </q-carousel>
</template>

<script>
export default {
  name: 'VoteMobile',
  props: {
    entries: {
      type: Array,
    },
    subject: {
      type: Object,
    },
  },
  emits: ['vote'],
  watch: {
    entries: function(newEntries) {
      this.slide = newEntries[0].id;
    },
  },
  data() {
    return {
      slide: this.entries[0].id,
      latestTap: null,
    };
  },
  mounted() {
    // TODO: log errors
    window.addEventListener('keyup', this.parseKeyboardVote);
  },
  methods: {
    registerVote(entryId) {
      this.$emit('vote', entryId);
    },
    registerTap(evt) {
      const currentTap = evt.timeStamp;
      if (currentTap - this.latestTap < 300) {
        this.registerVote(this.slide);
      }
      this.latestTap = currentTap;
    },
  },
};

</script>

<style scoped>
.photo-slide {
  max-width: 100%;
}

h1 {
  font-size: 72px;
  line-height:72px;
}
</style>
