import { getBreadCrumbList, setTagNavListInLocalstorage, getMenuByRouter, getTagNavListFromLocalstorage, getHomeRoute, getTheme, setTheme, getVersion, getSha1, setVersion, setSha1 } from '@/libs/util'
import routers from '@/router/routers'
export default {
    state: {
        breadCrumbList: [],
        tagNavList: [],
        homeRoute: getHomeRoute(routers),
        local: '',
        theme: getTheme(),
        version: getVersion(),
        sha1: getSha1()
    },
    getters: {
        menuList: (state, getters, rootState) => getMenuByRouter(routers, rootState.user.access),
        themeGetter: (state) => {
            return state.theme ? getTheme() : state.theme
        }
    },
    mutations: {
        setBreadCrumb(state, routeMetched) {
            state.breadCrumbList = getBreadCrumbList(routeMetched)
        },
        setTagNavList(state, list) {
            if (list) {
                state.tagNavList = [...list]
                setTagNavListInLocalstorage([...list])
            } else state.tagNavList = getTagNavListFromLocalstorage()
        },
        addTag(state, item, type = 'unshift') {
            if (typeof(item.name) === 'undefined') return
            if (state.tagNavList.findIndex(tag => tag.name === item.name) < 0) {
                if (type === 'push') state.tagNavList.push(item)
                else state.tagNavList.unshift(item)
                setTagNavListInLocalstorage([...state.tagNavList])
            }
        },
        setLocal(state, lang) {
            state.local = lang
        },
        setTheme(state, t) {
            state.theme = t
            setTheme(t)
        },
        setVersion(state, v) {
            state.version = v
            setVersion(v)
        },
        setSha1(state, s) {
            state.sha1 = s
            setSha1(s)
        },
    },
}
