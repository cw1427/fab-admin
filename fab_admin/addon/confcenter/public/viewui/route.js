export default    {
    path: '/conf',
    name: 'confcenter',
    meta: {
        icon: 'ios-flag',
        title: 'Config Center',
    },
    component: ()=>import('@/view/main'),
    children: [{
            path: '/conf/config',
            name: 'confCenter',
            meta: {
                icon: 'ios-flower',
                title: 'config',
                componentName: 'ConfCenter',
                access: ['Admin','configurer']
            },
            component: () => import('#/confcenter/public/viewui')
        },
        {
            path: '/conf/manage',
            name: 'confManage',
            meta: {
                icon: 'ios-flower',
                title: 'management',
                access: ['Admin', 'confmanager'],
                componentName: 'ConfCenterManage'
            },
            component: () => import('#/confcenter/public/viewui/confcentermanage.vue')
        }
    ]
}
