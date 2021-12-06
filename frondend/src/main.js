import Vue from 'vue';
import App from './App';
import router from './router'
import Antd from 'ant-design-vue'; // ui
import 'ant-design-vue/dist/antd.css'; // css
import 'echarts/map/js/world' // echart world

Vue.use(Antd);// use

Vue.config.productionTip = false;


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router: router,
  components: { App },
  template: '<App/>',
});
