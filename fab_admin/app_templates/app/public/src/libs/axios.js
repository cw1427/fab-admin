import Axios from 'axios'
import baseURL from '_conf/url'
import { Message, Spin } from 'iview'
import router from '@/router'
import { setToken } from '@/libs/util'
import Cookies from 'js-cookie'
import { TOKEN_KEY } from '@/libs/util'
class httpRequest {
    constructor() {
        this.options = {
            method: '',
            url: ''
        }
        this.queue = {}
    }

    destroy(url) {
            delete this.queue[url]
            const queue = Object.keys(this.queue)
            return queue.length
        }
        // request interceptor
    interceptors(instance, url) {
        instance.interceptors.request.use(config => {
            // if (!config.url.includes('/users')) {
            //     config.headers['x-access-token'] = Cookies.get(TOKEN_KEY)
            // }
            // Spin.show()
            return config
        }, error => {
            // Spin.hide()
            return Promise.reject(error)
        })

        instance.interceptors.response.use((res) => {
            const is = this.destroy(url)
            if (!is) {
                setTimeout(() => {
                    Spin.hide()
                }, 500)
            }
            return res
        }, (error) => {
            // Spin.hide()
            if (error.response) {
                if (error.response.status >= 500) {
                    Message.error('Internal error')
                }
                if (error.response.status == 401) {
                    setToken('')
                    Message.error('Require login')
                        //----do the redirect to login
                    router.push({
                        name: 'login'
                    })
                }
            } else {
                Message.error(error.message)
                error.response = {}
                error.response.data = { 'status': 'unknown', 'message': 'Error occurred' }
            }
            return Promise.reject(error)
        })
    }

    create() {
        let conf = {
            baseURL: baseURL,
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            validateStatus: function(status) {
                return status < 500; // Reject only if the status code is greater than or equal to 400
            },
            withCredentials: true
        }
        return Axios.create(conf)
    }
    mergeReqest(instances = []) {
        //
    }
    request(options) {
        var instance = this.create()
        this.interceptors(instance, options.url)
        options = Object.assign({}, options)
        this.queue[options.url] = instance
        return instance(options)
    }
}
export default httpRequest