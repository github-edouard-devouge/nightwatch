<template>
  <div id="cards">
    <b-spinner v-if="showOverlay" variant="dark" label="Loading"></b-spinner>
    <b-overlay variant="dark" :show="showOverlay" rounded="sm">
    <p style="text-align: left; margin-left: 20px;"><b>Watch findinds: </b><b-avatar size="3rem" variant="danger">{{ images.length }}</b-avatar> new tags <b-icon icon="tag-fill" variant="dark"></b-icon></p>
      <b-card style="margin: 20px 20px 20px 20px;" v-for="image in images" :key="image.uuid" no-body class="overflow-hidden">
        <b-row  align-v="center" no-gutters>
          <b-col md="1">
            <b-card-img style="margin: 0 20px;" :src="require('../assets/docker.png')" alt="Image" ></b-card-img>
          </b-col>
          <b-col>
            <b-card-body style="text-align: left; margin: 20px;">
              <h3><b-link :to="`image/${image.uuid}`" class="link">{{image.repository}}</b-link></h3>
              <b-button :id="`popover-0-${image.uuid}`" size="sm" :href="`${getRegistryLink(image.uuid)}`" target="_blank">
                {{image.registry.name}}
              </b-button>
              <b-popover :target="`popover-0-${image.uuid}`" triggers="hover" placement="top">
                Open {{image.repository}} repository details in a new tab
              </b-popover>
            </b-card-body>
          </b-col>
          <b-col md="3">
            <h4 :id="`popover-1-${image.uuid}`">Current tag: <b-badge variant="secondary">{{image.currentTag.name}}</b-badge></h4>
            <b-popover :target="`popover-1-${image.uuid}`" triggers="hover" placement="top">
              <template v-slot:title><b-icon icon="tag-fill" variant="dark"></b-icon> Tag release date:</template>
              <p style="text-align:center;"><b-icon icon="calendar2" variant="dark"></b-icon> {{image.currentTag.start_ts | formatDate}}</p>
            </b-popover>
          </b-col>
          <b-col md="3">
            <h4 :id="`popover-2-${image.uuid}`">Recent tag: <b-badge  variant="danger">{{image.targetTag.name}}</b-badge></h4>
            <b-popover :target="`popover-2-${image.uuid}`" triggers="hover" placement="top">
              <template v-slot:title><b-icon icon="tag-fill" variant="dark"></b-icon> Tag release date:</template>
              <p style="text-align:center;"><b-icon icon="calendar2" variant="dark"></b-icon> {{image.targetTag.start_ts | formatDate}}</p>
            </b-popover>
          </b-col>
        </b-row>
      </b-card>
    </b-overlay>
  </div>
</template>

<script>

import NightWatchDataService from "../services/NightWatchDataService";

export default {
  data(){
    return {
        showOverlay: true,
        timer: null,
        last_watch: null,
        last_watch2: null,
        images: []
    }
  },
  methods: {
    getRegistryLink(uuid) {
      for (const image of this.images) {
        if(image.uuid == uuid){
          if(image.registry.name == "docker.io"){
            return "https://hub.docker.com/r/"+image.repository+"/tags"
          }
          else if(image.registry.name == "quay.io"){
            return "https://quay.io/repository/"+image.repository+"?tab=tags"
          }
          else return "#"
        }
      }

    },
    toastInfo(info) {
      this.$bvToast.toast(info, {
        title: 'Info',
        autoHideDelay: 5000,
        variant: 'dark',
        solid: true
      })
    },
    loadStatus(){
      NightWatchDataService.getStatus()
      .then(response => (this.last_watch2 = response['data']['last_watch']))
      if(this.last_watch2 && this.last_watch2 != this.last_watch){
        this.loadImages()
        this.last_watch = this.last_watch2
      }
    },
    loadImages(){
      this.showOverlay = true
      NightWatchDataService.getOutdatedImages()
      .then(
        response => (this.images =  response['data'])
      )
      this.showOverlay = false
    }
  },
  mounted () {
    NightWatchDataService.getStatus()
    .then(response => (this.last_watch = response['data']['last_watch']))
    this.loadImages()
    this.timer = setInterval(this.loadStatus, 10000);
  }
}
</script>

<style scoped>
  a:link.link {
    color: #343a40;
    text-decoration: none;
  }

  a:visited.link {
    color: #343a40;
    text-decoration: none;
  }

  a:hover.link  {
    color: #dc3545;
    text-decoration: none;
  }

  a:active.link  {
    color: #dc3545;
    text-decoration: none;
  }

  .row:hover {
    background-color: #EFEFEF;
  }
</style>
