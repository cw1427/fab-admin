import Cookies from 'js-cookie'
import config from '@/config'
import { forEach, hasOneOf, getRouterObjByName } from '@/libs/tools'

export const TOKEN_KEY = config.TOKEN_KEY

export const setToken = (token) => {
    Cookies.set(TOKEN_KEY, token, { expires: config.cookieExpires || 1 })
}

export const getToken = () => {
    const token = Cookies.get(TOKEN_KEY)
    if (token) return token
    else return false
}

export const hasChild = (item) => {
    return item.children && item.children.length !== 0
}

const showThisMenuEle = (item, access) => {
        if (item.meta && item.meta.access && item.meta.access.length) {
            if (hasOneOf(item.meta.access, access)) return true
            else return false
        } else return true
    }
    /**
     * @param {Array} list get all the menu list from the router
     * @returns {Array}
     */
export const getMenuByRouter = (list, access) => {
    let res = []
    forEach(list, item => {
        if (item.meta && !item.meta.hideInMenu) {
            let obj = {
                icon: (item.meta && item.meta.icon) || '',
                name: item.name,
                meta: item.meta
            }
            if (hasChild(item) && showThisMenuEle(item, access)) {
                obj.children = getMenuByRouter(item.children, access)
            }
            if (showThisMenuEle(item, access)) res.push(obj)
        }
    })
    return res
}

/**
 * @param {Array} routeMetched metched current route
 * @returns {Array}
 */
export const getBreadCrumbList = (routeMetched) => {
    let res = routeMetched.filter(item => {
        return item.meta === undefined || !item.meta.hide
    }).map(item => {
        let obj = {
            icon: (item.meta && item.meta.icon) || '',
            name: item.name,
            meta: item.meta
        }
        return obj
    })
    res = res.filter(item => {
        return !item.meta.hideInMenu
    })
    return [{
        name: 'home',
        to: '/home'
    }, ...res]
}

export const showTitle = (item, vm) => vm.$config.useI18n ? vm.$t(item.name) : ((item.meta && item.meta.title) || item.name)

/**
 * @description store the Tag list in local
 */
export const setTagNavListInLocalstorage = list => {
        localStorage.tagNaveList = JSON.stringify(list)
    }
    /**
     * @returns {Array} restore the Tag list from localstore: name, path, meta
     */
export const getTagNavListFromLocalstorage = () => {
    const list = localStorage.tagNaveList
    return list ? JSON.parse(list) : []
}

/**
 * @param {Array} routers
 * @description find the home route
 */
export const getHomeRoute = routers => {
    let i = -1
    if (routers == null) return {}
    let len = routers.length
    let homeRoute = {}
    while (++i < len) {
        let item = routers[i]
        if (item.children && item.children.length) {
            let res = getHomeRoute(item.children)
            if (res.name) return res
        } else {
            if (item.name === 'home') homeRoute = item
        }
    }
    return homeRoute
}

/**
 * @param {*} list get new Tag list
 * @param {*} newRoute new Tag route
 * @description check if exists in the Tag list, if not then add it
 */
export const getNewTagList = (list, newRoute) => {
    const { name, path, meta } = newRoute
    let newList = [...list]
    if (newList.findIndex(item => item.name === name) >= 0) return newList
    else newList.push({ name, path, meta })
    return newList
}

/**
 * @param {*} access Check user access permission: ['super_admin', 'admin']
 * @param {*} route
 */
const hasAccess = (access, route) => {
    if (route.meta && route.meta.access) return hasOneOf(access, route.meta.access)
    else return true
}

/**
 * @param {*} name to route name
 * @param {*} access use access group
 * @param {*} routes Vue router obj
 * @description check if user have access permission for {to}
 */
export const canTurnTo = (name, access, routes) => {

    let route = getRouterObjByName(null, routes, name)
    const checkHasAccessRoutenames = (route) => {
        if (route.parent && route.parent != null) {
            if (!checkHasAccessRoutenames(route.parent)) return false
        }
        if (route.meta && route.meta.access) {
            if (!hasAccess(access, route)) return false
        }
        return true
    }
    return checkHasAccessRoutenames(route)
}

/**
 * @param {String} url
 * @description get params from url
 */
export const getParams = url => {
    const keyValueArr = url.split('?')[1].split('&')
    let paramObj = {}
    keyValueArr.forEach(item => {
        const keyValue = item.split('=')
        paramObj[keyValue[0]] = keyValue[1]
    })
    return paramObj
}

/**
 * @param {Array} list The Tag list
 * @param {String} name current to be closed Tag name
 */
export const getNextName = (list, name) => {
    let res = ''
    if (list.length === 2) {
        res = 'home'
    } else {
        if (list.findIndex(item => item.name === name) === list.length - 1) res = list[list.length - 2].name
        else res = list[list.findIndex(item => item.name === name) + 1].name
    }
    return res
}

/**
 * @param {Number} times execute times
 * @param {Function} callback callback function
 */
export const doCustomTimes = (times, callback) => {
    let i = -1
    while (++i < times) {
        callback()
    }
}


export const findNodeUpper = (ele, tag) => {
    if (ele.parentNode) {
        if (ele.parentNode.tagName === tag.toUpperCase()) {
            return ele.parentNode
        } else {
            return findNodeUpper(ele.parentNode, tag)
        }
    }
}

export const findNodeDownward = (ele, tag) => {
    const tagName = tag.toUpperCase()
    if (ele.childNodes.length) {
        let i = -1
        let len = ele.childNodes.length
        while (++i < len) {
            let child = ele.childNodes[i]
            if (child.tagName === tagName) return child
            else return findNodeDownward(child, tag)
        }
    }
}

export const showByAccess = (access, canViewAccess) => {
    return hasOneOf(canViewAccess, access)
}

export const getTheme = () => {
    const theme = localStorage.theme
    return theme ? theme : 'dark'
}

export const setTheme = (theme) => {
    localStorage.theme = theme
}

export const isEmptyObject = (e) => {
    var t;
    for (t in e)
        return !1;
    return !0
}

export const getVersion = () => {
    const v = localStorage.version
    return v ? v : ''
}

export const setVersion = (v) => {
    localStorage.version = v
}

export const getSha1 = () => {
    const v = localStorage.sha1
    return v ? v : ''
}

export const setSha1 = (v) => {
    if (v) {
        localStorage.sha1 = v
    }
}

export const loadFabadminAddonRoute=() =>{
    const addonRoutes=[]
    config.fabadmin_addons.forEach((v)=>{
        const route = require('#/'+v+'/public/viewui/route.js')
        addonRoutes.push(route.default)
    })
    return addonRoutes
}
