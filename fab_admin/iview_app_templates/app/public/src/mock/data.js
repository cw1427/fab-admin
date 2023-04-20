import Mock from 'mockjs'

export const getConfProjects = req => {
    let projs = ['proj1', 'proj2']
    return {
        status: 200,
        data: projs,
        msg: ''
    }
}