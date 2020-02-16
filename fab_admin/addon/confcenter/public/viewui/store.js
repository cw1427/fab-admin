export default {
    state: {
        basePath: ''
    },
    mutations: {
        setBasePath(state, base) {
            state.basePath = base
        },

    },
    actions: {
        handleBasePath({ commit }, basePath) {
            if (typeof(basePath) === 'undefined') return;
            basePath = basePath.trim()
            commit('setBasePath', basePath.split('/')[1])
        }
    }

}