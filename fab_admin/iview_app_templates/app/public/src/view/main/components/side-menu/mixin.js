import CommonIcon from '_c/common-icon'
export default {
    components: {
        CommonIcon
    },
    methods: {
        showTitle(item) {
            return this.$config.useI18n ? this.$t(item.name) : ((item.meta && item.meta.title) || item.name)
        },
        showChildren(item) {
            return item.children && item.children.length >= 1
        }
    }
}
