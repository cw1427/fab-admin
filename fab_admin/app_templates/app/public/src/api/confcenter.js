import axios from '@/libs/api.request'
import store from '@/store'

export const getProjects = () => {
    return axios.request({
        url: store.state.confcenter.basePath + '/api/getprojects',
        method: 'get'
    })
}

export const getConfigs = (proj) => {
    return axios.request({
        url: store.state.confcenter.basePath + '/api/getallconfig/' + proj,
        method: 'get'
    })
}

export const addOrEditConfig = (params) => {
    let url = store.state.confcenter.basePath + '/api/addconfig/' + params.proj
    if (params.editable) {
        url = store.state.confcenter.basePath + '/api/updateconfig/' + params.proj
    }
    return axios.request({
        url: url,
        data: params,
        method: 'post'
    })
}

export const addProject = (proj) => {
    return axios.request({
        url: store.state.confcenter.basePath + '/api/addproject/' + proj,
        method: 'get'
    })
}

export const getProjPerm = (proj) => {
    return axios.request({
        url: store.state.confcenter.basePath + '/api/getpermission/' + proj,
        method: 'get'
    })
}

export const updateProjPerm = (params) => {
    return axios.request({
        url: store.state.confcenter.basePath + '/api/updatepermission/' + params.proj,
        data: params,
        method: 'post'
    })
}

export const deleteConfItem = (params) => {
    return axios.request({
        url: store.state.confcenter.basePath + '/api/delconfig/' + params.proj + '/' + params.name,
        data: params,
        method: 'delete'
    })
}

export const deleteConfProj = (params) => {
    return axios.request({
        url: store.state.confcenter.basePath + '/api/delproj/' + params.proj,
        data: params,
        method: 'delete'
    })
}