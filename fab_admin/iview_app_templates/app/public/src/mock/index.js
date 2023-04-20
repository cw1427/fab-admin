import Mock from 'mockjs'
import { getConfProjects } from './data'

Mock.mock(/conf\/api\/getprojects/, 'get', getConfProjects)


export default Mock