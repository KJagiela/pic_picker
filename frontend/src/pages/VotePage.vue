<template>
  <div v-if="entries">
    <div class="desktop-only">
      <VoteDesktop :entries="entries" :subject="subject" @vote="registerVote"/>
    </div>
    <div class="mobile-only">
      <VoteMobile :entries="entries" :subject="subject" @vote="registerVote"/>
    </div>
  </div>
  <div v-else class="row justify-center">
    Nie masz już żadnych zdjęć do oceny w tym challenge'u ;)
  </div>
</template>

<script>
import {Cookies} from 'quasar';
import {api} from 'boot/axios';
import VoteDesktop from 'components/VoteDesktop.vue';
import VoteMobile from 'components/VoteMobile.vue';
// TODO: enhance photo

export default {
  name: 'VotePage',
  components: {VoteDesktop, VoteMobile},
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
  },
  methods: {
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
    // TODO: optimize, its slow AF
    getPicks() {
      api
          .get(
              `available_picks/?challenge_id=${this.challengeId}`,
              {
                headers: {Authorization: `Token ${this.token}`},
              },
          )
          .then((response) => {
            if (response.status === 226) {
              this.$router.push({name: 'results'});
            }
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

</style>
