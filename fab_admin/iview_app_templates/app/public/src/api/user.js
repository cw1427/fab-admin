import axios from '@/libs/api.request'

export const login = ({ userName, password }) => {
    const data = {
        userName,
        password
    }
    return axios.request({
        url: 'api/login',
        data,
        method: 'post'
    })
}

export const getUserInfo = (token) => {
    return axios.request({
        url: 'api/user_info',
        params: {
            token
        },
        method: 'get'
    })
}

export const logout = (token) => {
    return axios.request({
        url: 'api/logout',
        method: 'post'
    })
}

export const getUserList = (params) => {
    return axios.request({
        url: 'api/user_list',
        data: params,
        method: 'post'
    })
}

export const deleteUserById = (params) => {
    return axios.request({
        url: 'api/user_delete',
        data: params,
        method: 'post'
    })
}

export const selfUpdateUser = (params) => {
    return axios.request({
        url: 'api/self_user_update',
        data: params,
        method: 'post'
    })
}

export const resetMypassword = (params) => {
    return axios.request({
        url: 'api/reset_mypassword',
        data: params,
        method: 'post'
    })
}

export const genApikey = () => {
    return axios.request({
        url: 'userapikey/api/gen',
        method: 'get'
    })
}

export const getAllUsers = () => {
    return axios.request({
        url: 'api/get_all_users',
        method: 'get'
    })
}

export const getAutoDoc = (params) => {
    return axios.request({
        url: 'autodoc/api/' + params.group,
        method: 'get'
    })
}

export const editUser = (params) => {
    return axios.request({
        url: 'api/user_update',
        data: params,
        method: 'post'
    })
}

export const getAllRoles = () => {
    return axios.request({
        url: 'api/get_all_roles',
        method: 'get'
    })
}

export const addUser = (params) => {
    return axios.request({
        url: 'api/add_user',
        data: params,
        method: 'post'
    })
}

export const syncLdapUser = (params) => {
    return axios.request({
        url: 'api/sync_ldap_user',
        data: params,
        method: 'post'
    })
}
