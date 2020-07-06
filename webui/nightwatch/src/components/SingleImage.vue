<template>
  <div id="SingleImage">
    <b-card no-body class="overflow-hidden cards">
      <b-row  align-v="center" no-gutters>
        <b-col md="1">
          <b-card-img style="margin: 0 20px;" :src="require('../assets/docker.png')" alt="Image" ></b-card-img>
        </b-col>

        <b-col>
          <b-card-body style="text-align: left; margin: 20px;">
            <h3>{{image.repository}}</h3>
            <b-button :id="`popover-0-${image.uuid}`" size="sm" :href="getRegistryLink()" target="_blank">
              {{image.registry.name}}
            </b-button>
            <b-popover :target="`popover-0-${image.uuid}`" triggers="hover" placement="top">
              Open repository details in a new tab
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
    <b-card header-tag="header" class="overflow-hidden cards">
      <template v-slot:header>
        <h5 class="mb-0">Tag release history</h5>
      </template>
      <b-row   no-gutters>
        <b-col md="3">
          <Timeline :timeline-items="timelineItems" order="desc"/>
        </b-col>
      </b-row>
    </b-card>
  </div>
</template>

<script>

import NightWatchDataService from "../services/NightWatchDataService";
import Timeline from 'timeline-vuejs'
import moment from 'moment'

export default {
  name: 'SingleImage',
  components: {
    Timeline
  },
  data(){
    return {
        image: {},
        timelineItems: []
    }
  },
  methods: {
    getRegistryLink() {
        if(this.image.registry.name == "docker.io"){
          return "https://hub.docker.com/r/"+this.image.repository+"/tags"
        }
        else if(this.image.registry.name == "quay.io"){
          return "https://quay.io/repository/"+this.image.repository+"?tab=tags"
        }
        else return "#"
    },
    toastInfo(info) {
      this.$bvToast.toast(info, {
        title: 'Info',
        autoHideDelay: 5000,
        variant: 'dark',
        solid: true
      })
    },
    loadImage(callback){
      NightWatchDataService.getImage(this.$route.params.image_uuid)
      .then(
        response => (this.buildTimelineData(response['data']))
      )
      callback()
    },
    buildTimelineData(image){
      this.image = image
      const timelineItems = []

      for (const tag of image.availableTags) {
        var badgecolor= '#343a40'
        if(tag.name == image.currentTag.name || tag.name == image.targetTag.name){
          badgecolor = '#dc3545';
        }
        const timelineItem = {
          from: new Date(tag.start_ts),
          title: "<h4>"+tag.name+"</h4>",
          description: moment(String(tag.start_ts)).format('DD/MM/YYYY HH:mm'),
          color: badgecolor
        }
        timelineItems.push(timelineItem)
      }
      this.timelineItems = timelineItems
      return timelineItems
    }
  },
  mounted () {
    this.loadImage()
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

.wrapper-item{
  margin-bottom: 1px;
}
.cards {
  margin: 20px 20px 20px 20px;
}
</style>
