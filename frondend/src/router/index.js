import Vue from 'vue'
import Router from 'vue-router'
import Epidemic from '@/components/Epidemic'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Epidemic',
      component: Epidemic
    }
  ]
})
