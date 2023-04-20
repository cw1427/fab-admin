<style lang="less">
  @import './login.less';
</style>

<template>
<div :style="'height:880px; background-image: url(' + slide1 + ');  background-size: 100%'">
   <Row style="height:80px">
   <Col span="24">
      <index-header></index-header>
    </Col>
   </Row>
<section id="autodoc">
 <Row style="height:800px" :gutter="16">
   <Col span="13" offset="3" class="">
    <div class="slide">
      <index-slider :key="key"></index-slider>
    </div>
   </Col>
   <Col span="5">
      <div class="login" @keydown.enter="handleLogin">
        <div class="login-con">
          <Card icon="log-in" title="Welcome" :bordered="false">
            <div class="form-con">
              <login-form @on-success-valid="handleSubmit"></login-form>
              <p class="login-tip">Please input moto coreid password</p>
            </div>
          </Card>
        </div>
      </div>
    </Col>
 </Row>
</section>

<section id="feature">
  <div id="best-deal">
    <Row style="padding: 7em 0" :gutter="10">
      <Col span="3" offset="3">
        <Card style="width:320px;height:400px;">
            <div style="text-align:center">
                <img :src="jenkins">
                 <p class="fh5co-property-specification">
                  <h4>Jenkins module</h4>
                 </p>
            </div>
        </Card>
      </Col>
      <Col span="3" offset="3">
        <Card style="width:320px;height:400px;">
            <div style="text-align:center">
                <img :src="artifactory">
                <p class="fh5co-property-specification">
                  <h4>Download upload benchmark</h4>
                </p>
            </div>
        </Card>
      </Col>
      <Col span="3" offset="3">
        <Card style="width:320px;height:400px;">
            <div style="text-align:center">
                <img :src="confcenter">
                <p class="fh5co-property-specification">
                 <h4>Config data management</h4>
                 <h4>Retrive data via RESTAPI</h4>
                </p>
            </div>
        </Card>
      </Col>
    </Row>
  </div>
</section>

  <footer id="fh5co-footer" role="contentinfo">
        <div class="fh5co-copyright text-center">
                &copy; since 2020 {* app_name *} team All Rights Reserved. <span>Designed with</span>
            </div>
  </footer>

    <BackTop :height="50" :bottom="200">

    </BackTop>
 </div>
</template>

<script>
import LoginForm from '_c/login-form'
import { mapActions } from 'vuex'
import { Message,LoadingBar } from 'iview'
import IndexHeader from './components/index-header.vue'
import IndexSlider from './components/index-slider.vue'
import slide1 from '@/assets/images/slide_1.jpg'
import jenkins from '@/assets/images/jenkins_image.jpg'
import artifactory from '@/assets/images/artifactory_logo.jpg'
import confcenter from '@/assets/images/confcenter.jpg'

export default {
  components: {
    LoginForm,
    IndexHeader,
    IndexSlider
  },

  data() {
    return {
       slideIndex:0,
       slide1,
       jenkins,
       artifactory,
       confcenter,
       key:this.$route.path
    }
  },

  methods: {
    ...mapActions([
      'handleLogin',
      'getUserInfo'
    ]),
    handleSubmit ({ userName, password }) {
        LoadingBar.start();
        this.handleLogin({ userName, password }).then(res => {
          this.getUserInfo().then(res => {
            LoadingBar.finish();
            this.$router.push({
              name: 'main'
            })
          })
        }).catch( err => {
            LoadingBar.error();
            if (err.response){
                Message.error(err.response.data.msg,10)
            }else{
                Message.error(err.data.msg,10)
            }
          })
    },
  }
}
</script>

<style>

</style>
