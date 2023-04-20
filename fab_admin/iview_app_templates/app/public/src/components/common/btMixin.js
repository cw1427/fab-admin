import Vue from 'vue/dist/vue.js';
import iView from 'iview'
import i18n from '@/locale'

/*
* bootstrat-table VUE formatter mixin
*/

export default {
    data () {
      return {
        vueFormatters: []
      }
    },
  
    methods: {
      vueFormatter (obj) {
        const key = `_vue_formatter_${this.vueFormatters.length}`
        this.vueFormatters.push({
          el: `.${key}`,
          name: key,
          ...obj
        })
        return `<div class="${key}"/>`
      },
  
      vueFormatterPostBody () {
        if (!this.vueFormatters.length) {
          return
        }
  
        for (let i = this.vueFormatters.length - 1; i >= 0; i--) {
          const formatter = this.vueFormatters[i]
  
          if (document.getElementsByClassName(formatter.name)) {
            Vue.use(iView, {
                i18n: (key, value) => i18n.t(key, value)
            })
            new Vue(formatter)
            this.vueFormatters.splice(i, 1)
          }
        }
      }
    }
  }