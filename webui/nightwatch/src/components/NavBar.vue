<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark">
      <b-navbar-brand href="/">
        <b-avatar size="3rem" variant="danger"><b-icon icon="eye-fill" variant="white"></b-icon></b-avatar> NIGHTWATCH
      </b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/findings">Findings</b-nav-item>
          <b-nav-item to="/images">All images</b-nav-item>
        </b-navbar-nav>
        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-card style="margin: 1px;" bg-variant="dark" text-variant="white" class="text-center">
            <b-icon icon="eye" variant="white"></b-icon> Last watch: {{ backendState.last_watch | formatDate }}
          </b-card>
          <b-button v-show="backendState.watching" variant="dark">
            <b-spinner  label="Watching" variant="danger" ></b-spinner>  Watch in progress...
          </b-button>
          <b-button v-show="!backendState.watching" variant="secondary" v-on:click="watch">
            <b-icon icon="arrow-counterclockwise" variant="white"></b-icon>
            Start a new watch
          </b-button>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import NightWatchDataService from "../services/NightWatchDataService";

export default {
  data(){
    return {
        backendState: [],
        timer: null
    }
  },
  methods: {
    toastInfo(info) {
      this.$bvToast.toast(info, {
        title: 'Info',
        autoHideDelay: 5000,
        variant: 'dark',
        solid: true
      })
    },
    toastError(error) {
      this.$bvToast.toast(error, {
        title: 'Error',
        autoHideDelay: 5000,
        variant: 'danger',
        solid: true
      })
    },
    watch() {
      NightWatchDataService.watch()
      .then(
        this.backendState.watching = true
      )
      .catch(errors => {
        this.toastError("[ERROR] Could not join API backend: " + errors);
      })
    },
    loadStatus(){
      NightWatchDataService.getStatus()
      .then(response => (this.backendState = response['data']))
      .catch(errors => {
        this.toastError("[ERROR] Could not join API backend: " + errors);
      })
    }
  },
  mounted () {
    this.loadStatus()
    this.timer = setInterval(this.loadStatus, 5000);
  }
}
</script>
