import Vue from 'vue'
import Router from 'vue-router'
import routes from './routers'
import store from '@/store'
import iView from 'iview'
import { getToken, canTurnTo } from '@/libs/util'

Vue.use(Router)
const router = new Router({
    routes
})
const LOGIN_PAGE_NAME = 'login'

router.beforeEach((to, from, next) => {
    iView.LoadingBar.start()
    const token = getToken()
    if (!token && to.name !== LOGIN_PAGE_NAME) {
        next({
            name: LOGIN_PAGE_NAME // go to login
        })
    } else if (!token && to.name === LOGIN_PAGE_NAME) {
        next()
    } else if (token && to.name === LOGIN_PAGE_NAME) {
        next({
            name: 'main'
        })
    } else {
        //---already login---no need to fetch userInfo again
        if (store.state.user.userId.length == 0) {
            //-----go to get the userinfo
            store.dispatch('getUserInfo').then(res => {
                if (res.status == 302) {
                    //----lost the session need to redirect to login
                    store.commit('setToken', '')
                    next({
                        name: LOGIN_PAGE_NAME // go to login
                    })
                } else {
                    if (canTurnTo(to.name, store.state.user.access, routes)) next()
                    else next({ replace: true, name: 'error_401' })
                }
            })
        } else {
            if (canTurnTo(to.name, store.state.user.access, routes)) {
                if (['confCenter', 'confManage', 'credConfig', 'credManage'].indexOf(to.name) > -1) {
                    store.dispatch('handleBasePath', to.path)
                }
                next()
            } else next({ replace: true, name: 'error_401' })
        }
    }
})

router.afterEach(to => {
    iView.LoadingBar.finish()
    window.scrollTo(0, 0)
})

export default router