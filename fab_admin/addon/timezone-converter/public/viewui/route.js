export default    {
    path: '/timezone',
    name: '',
    meta: {
        //hideInMenu: true,
        icon: 'md-clock',
        title: 'Timezone',
    },
    component: ()=>import('@/view/main'),
    children: [{
        path: '',
        name: 'timezone',
        meta: {
            icon: 'ios-flower',
            title: 'Timezone Converter',
        },
        component: ()=> import ('#/timezone-converter/public/viewui/timezone-converter.vue')
    }]
}
