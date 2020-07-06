<template>
  <div id="table">
    <p style="text-align: left; margin-left: 20px;"><b>Watch findinds: </b><b-avatar size="3rem" variant="danger">{{ images.length }}</b-avatar> deployed images tags in the kubernetes cluster <b-icon icon="tag-fill" variant="dark"></b-icon></p>
    <b-table class="text-left" striped hover :items="images" :fields="fields" outlined></b-table>
  </div>
</template>
<script>
import NightWatchDataService from "../services/NightWatchDataService";
export default {
  data(){
    return {
        timer: null,
        last_watch: null,
        last_watch2: null,
        images: [],
        fields: ['registry.name', 'repository', "currentTag.name", 'targetTag.name']
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
      NightWatchDataService.getAllImages()
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
