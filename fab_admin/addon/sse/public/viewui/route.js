export default {
        path: '/sse',
        name: 'sse',
        meta: {
            icon: 'md-construct',
            title: 'SSE sample',
            // hide: true,
            // hideInMenu: true,
            access: ['Admin']
        },
        component: ()=>import('@/view/main'),
        children: [{
                path: '/sse/sample',
                name: 'sse_sample',
                meta: {
                    icon: 'ios-people',
                    title: 'sample'
                },
                component:  () => import('#/sse/public/viewui')
                //component:  () => import ('@/view/sse')
        }]
}
