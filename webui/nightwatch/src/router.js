import Vue from "vue";
import VueRouter from 'vue-router'

import TableImages from '@/components/TableImages.vue'
import CardsImages from '@/components/CardsImages.vue'
import SingleImage from '@/components/SingleImage.vue'

// Install vue router
Vue.use(VueRouter)

const routes = [
  {
     path: '/',
     name: 'home',
     component: CardsImages,
  },
  {
     path: '/images',
     name: 'images',
     component: TableImages
  },
  {
     path: '/findings',
     name: 'Findings',
     component: CardsImages
  },
  {
    path: '/image/:image_uuid',
    name: 'SingleImage',
    component: SingleImage
  }
]

export default new VueRouter({
  mode: "history",
  routes // short for `routes: routes`
})
