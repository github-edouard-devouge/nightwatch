import Vue from 'vue'

import App from './App.vue'
import VueRouter from 'vue-router'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import moment from 'moment'
import router from './router'

import '../node_modules/timeline-vuejs/dist/timeline-vuejs.css'


// Install vue router
Vue.use(VueRouter)
// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.config.productionTip = false

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('DD/MM/YYYY HH:mm')
  }
});

new Vue({
  render: h => h(App),
  router
}).$mount('#app')
