<template>
  <q-card class="form-card fixed-center q-px-md">
    <q-card-section>
      <h3 class="form-text text-center">Kto będzie głosował?</h3>
      <q-input
          input-class="text-center"
          class="form-input q-py-md q-px-xl"
          maxlength="256"
          v-model="name"
          @keyup.enter="registerUser"
      />
    </q-card-section>
    <q-card-actions align="center">
      <q-btn class="submit-button" @click="registerUser">Zaczynamy!</q-btn>
    </q-card-actions>
  </q-card>

</template>

<script>
import {Cookies} from 'quasar';

import {api} from 'boot/axios';

export default {
  name: 'WelcomePage',
  data() {
    return {
      token: Cookies.get('auth_token'),
      name: '',
    };
  },
  mounted() {
    if (this.token) this.$router.push({name: 'vote'});
  },
  methods: {
    registerUser() {
      api.post(
          'users/',
          {username: this.name},
      )
          .then((response) => {
            this.token = response.data.token;
            let challenge = this.$route.query.challenge;
            if (!challenge) {
              challenge = '0d09f9e3-000d-43e6-b22e-06425d5838f9';
            }
            Cookies.set('auth_token', this.token);
            Cookies.set('challenge', challenge);
            this.$router.push({name: 'vote'});
          })
          .catch((response) => {
            console.error(response);
          });
    },
  },
};
</script>

<style scoped lang="scss">
.submit-button {
  color: $accent;
  background-color: $secondary;
}
.form-card {
  background-color: $accent;
}

.form-text {
  color: $secondary;
}
.form-input {
  font-size: 2em;
}
</style>
