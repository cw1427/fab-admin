<template>
  <Layout style="height: 100%" class="main">
    <Sider hide-trigger  collapsible :width="210" :collapsed-width="64" v-model="collapsed" :style="sideTheme">
      <side-menu accordion :active-name="$route.name" :collapsed="collapsed" @on-select="turnToPage" :menu-list="menuList" :theme="theme">
        <div class="logo-con" slot="header">
          <img v-show="!collapsed" :src="maxLogo" key="max-logo" />
          <img v-show="collapsed" :src="minLogo" key="min-logo" />
        </div>
      </side-menu>
      <div v-show="!collapsed" class="menufooter" width="210">
            <div class="line"  style="width:210px"></div>
            <div class="copyright"  style="width:210px">{* app_name *} Mobility © 2020 you.company,Inc. <br/> All Rights reserved.</div>
            <div style="text-align:center">
              <Row :gutter="4">
                <Col span="10">
                  <div class="copyright">{{version}}</div>
                </Col>
                <Col span="7">
                  <div class="copyright" v-if="sha1">{{sha1}}</div>
                </Col>
                <Col span="7">
                <a style="" href="/switch/original">Old UI</a>
                </Col>
              </Row>
            </div>
      </div>
    </Sider>
    <Layout>
      <Header class="header-con">
        <header-bar :collapsed="collapsed" @on-coll-change="handleCollapsedChange">
          <user :user-avator="userAvator"/>
          <language @on-lang-change="setLocal" style="margin-right: 10px;" :lang="local"/>
          <fullscreen v-model="isFullscreen" style="margin-right: 10px;"/>
          <Theme style="margin-right: 10px;"/>
        </header-bar>
      </Header>
      <Content>
        <Layout>
          <div class="tag-nav-wrapper">
            <tags-nav :value="$route" @input="handleClick" :list="tagNavList" @on-close="handleCloseTag"/>
          </div>
          <Content class="content-wrapper">
            <keep-alive :include="cacheList">
              <router-view :key="$route.path"/>
            </keep-alive>
          </Content>
        </Layout>
      </Content>
    </Layout>
  </Layout>
</template>
<script>
import SideMenu from './components/side-menu'
import HeaderBar from './components/header-bar'
import TagsNav from './components/tags-nav'
import User from './components/user'
import Fullscreen from './components/fullscreen'
import Language from './components/language'
import { mapMutations, mapActions } from 'vuex'
import { getNewTagList, getNextName } from '@/libs/util'
import minLogo from '@/assets/images/logo-min.jpg'
import maxLogo from '@/assets/images/logo.jpg'
import './main.less'
import Theme from './components/theme'
export default {
  name: 'Main',
  components: {
    SideMenu,
    HeaderBar,
    Language,
    TagsNav,
    Fullscreen,
    User,
    Theme
  },
  data () {
    return {
      collapsed: false,
      minLogo,
      maxLogo,
      isFullscreen: false,
      version: this.$store.state.app.version,
      sha1: this.$store.state.app.sha1,
    }
  },
  computed: {
    tagNavList () {
      return this.$store.state.app.tagNavList
    },
    tagRouter () {
      return this.$store.state.app.tagRouter
    },
    userAvator () {
      return this.$store.state.user.avatorImgPath
    },
    cacheList () {
      return this.tagNavList.length ? this.tagNavList.filter(item => !(item.meta && item.meta.notCache)).map(item =>{ return (typeof(item.meta.componentName) == 'undefined') ? item.name : item.meta.componentName} ): []
    },
    menuList () {
      return this.$store.getters.menuList
    },
    local () {
      return this.$store.state.app.local
    },
    theme() {
      return this.$store.state.app.theme
    },
    sideTheme () {
      if (this.theme == 'light'){
          return {background: '#fff'}
      }else{
          return null
      }
    }
  },
  methods: {
    ...mapMutations([
      'setBreadCrumb',
      'setTagNavList',
      'addTag',
      'setLocal'
    ]),
    ...mapActions([
      'handleLogin'
    ]),
    turnToPage (name) {
      this.$router.push({
        name: name
      })
    },
    handleCollapsedChange (state) {
      this.collapsed = state
    },
    handleCloseTag (res, type, name) {
      const nextName = getNextName(this.tagNavList, name)
      this.setTagNavList(res)
      if (type === 'all') this.turnToPage('main')
      else if (this.$route.name === name) this.$router.push({ name: nextName })
    },
    handleClick (item) {
      this.turnToPage(item.name)
    }
  },
  watch: {
    '$route' (newRoute) {
      this.setBreadCrumb(newRoute.matched)
      this.setTagNavList(getNewTagList(this.tagNavList, newRoute))
    }
  },
  mounted () {
    /**
     * @description init Tag nav list
     */
    this.setTagNavList()
    this.addTag(this.$store.state.app.homeRoute)
    this.setBreadCrumb(this.$route.matched)
    this.setLocal(this.$i18n.locale)
  }
}
</script>
