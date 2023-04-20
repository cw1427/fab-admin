import { login, logout, getUserInfo, getAllUsers, getAllRoles } from '@/api/user'
import { setToken, getToken } from '@/libs/util'

export default {
    state: {
        userName: '',
        firstName: '',
        lastName: '',
        userId: '',
        avatorImgPath: '',
        token: getToken(),
        access: '',
        loginName: '',
        email: '',
        userType: '',
        apiKey: '',
        lastLogin: '',
        allUsers: [],
        allRoles: []
    },
    mutations: {
        setAvator(state, avatorPath) {
            state.avatorImgPath = avatorPath
        },
        setUserId(state, id) {
            state.userId = id
        },
        setUserName(state, name) {
            state.userName = name
        },
        setLoginName(state, name) {
            state.loginName = name
        },
        setAccess(state, access) {
            state.access = access
        },
        setToken(state, token) {
            state.token = token
            setToken(token)
        },
        setFirstName(state, name) {
            state.firstName = name
        },
        setLastName(state, name) {
            state.lastName = name
        },
        setEmail(state, email) {
            state.email = email
        },
        setUserType(state, ut) {
            state.userType = ut
        },
        setApiKey(state, key) {
            state.apiKey = key
        },
        setLastLogin(state, key) {
            state.lastLogin = key
        },
        setAllUsers(state, key) {
            state.allUsers = key
        },
        setAllRoles(state, key) {
            state.allRoles = key
        },
    },
    actions: {
        handleLogin({ commit }, { userName, password }) {
            if (typeof(userName) === 'undefined') return;
            userName = userName.trim()
            return new Promise((resolve, reject) => {
                login({
                    userName,
                    password
                }).then(res => {
                    const data = res.data
                    if (res.status === 200) {
                        commit('setToken', data.token)
                        commit('setVersion', data.version)
                        commit('setSha1', data.sha1)
                    } else {
                        reject(res)
                    }
                    resolve(res)
                }).catch(err => {
                    reject(err)
                })
            })
        },
        // 退出登录
        handleLogOut({ state, commit }) {
            return new Promise((resolve, reject) => {
                logout(state.token).then(() => {
                    commit('setToken', '')
                    commit('setAccess', [])
                    resolve()
                }).catch(err => {
                    reject(err)
                })
            })
        },
        getUserInfo({ state, commit }) {
            return new Promise((resolve, reject) => {
                getUserInfo(state.token).then(res => {
                    if (res.status == 200) {
                        let data = res.data
                        commit('setAvator', data.avator)
                        commit('setUserName', data.user_name)
                        commit('setUserId', data.user_id)
                        commit('setAccess', data.access)
                        commit('setLoginName', data.login_name)
                        commit('setFirstName', data.first_name)
                        commit('setLastName', data.last_name)
                        commit('setEmail', data.email)
                        commit('setUserType', data.user_type)
                        commit('setLastLogin', data.last_login)
                        commit('setApiKey', data.api_key)
                    }
                    if (res.status >= 400) {
                        reject(res)
                    }
                    resolve(res)
                }).catch(err => {
                    reject(err)
                })
            })
        },
        getAllUsers({ state, commit }) {
            return new Promise((resolve, reject) => {
                getAllUsers().then(res => {
                    if (res.status == 200) {
                        commit('setAllUsers', res.data.data)
                    }
                    if (res.status >= 400) {
                        reject(res)
                    }
                    resolve(res)
                }).catch(err => {
                    reject(err)
                })
            })
        },
        getAllRoles({ state, commit }) {
            return new Promise((resolve, reject) => {
                getAllRoles().then(res => {
                    if (res.status == 200) {
                        commit('setAllRoles', res.data.data)
                    }
                    if (res.status >= 400) {
                        reject(res)
                    }
                    resolve(res)
                }).catch(err => {
                    reject(err)
                })
            })
        }
    }
}
