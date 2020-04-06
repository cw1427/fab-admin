// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import iView from 'iview'
import i18n from '@/locale'
import config from '@/config'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.min.css'
import 'bootstrap-table/dist/bootstrap-table.min.css'
import 'bootstrap-table/dist/themes/materialize/bootstrap-table-materialize.min.css'
import 'iview/dist/styles/iview.css'
import 'font-awesome/css/font-awesome.css'
import '@/assets/icons/iconfont.css'
import env from '../config/env'
import VueJsonPretty from 'vue-json-pretty'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/js/bootstrap.min.js'
//import Bootstrap from 'bootstrap'
import 'bootstrap-table/dist/bootstrap-table.min.js'
//import 'bootstrap-table'
import BootstrapTable from 'bootstrap-table/dist/bootstrap-table-vue.min.js'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Message.config({duration:5})

Vue.use(iView, {
    i18n: (key, value) => i18n.t(key, value)
})
Vue.use(BootstrapVue)
Vue.prototype.$Message.config({duration:5})
Vue.component('VueJsonPretty',VueJsonPretty)
Vue.component('BootstrapTable', BootstrapTable)
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.config.productionTip = false
    /**
     * @description global configuration
     */
Vue.prototype.$config = config
    // localStorage.clear();
    /* eslint-disable no-new */

new Vue({
    el: '#app',
    router,
    i18n,
    store,
    render: h => h(App)
})
