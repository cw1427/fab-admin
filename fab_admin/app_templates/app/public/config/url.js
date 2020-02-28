import env from './env'

const DEV_URL = 'http://{* address *}:8081/'
const PRO_URL = 'http://{* address *}:8080/'

export default env === 'development' ? DEV_URL : PRO_URL
