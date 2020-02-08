<template>
  <Row type="Flex">
    <Row >
      <Col span="12">
            <user-card :user-name="userName" :user-id="userId" :accesses="access" :login-name="loginName"></user-card>
      </Col>
      <Col span="12" >
          <!--<div> <Alert align="middle" class="welcome-message">Welcome to {* app_name *}</Alert></div>-->
           <Card style="height:300px">
              <p slot="title">
                  <Icon type="ios-film-outline"></Icon>
                  Welcome to {* app_name *} {{appVersion}}
              </p>

              <Tabs value="name1" type="card">
                  <TabPane label="Basic Authentication" name="name1">
                    <ul>
                        <li><common-icon type="_bulb" /> use curl/wget command paramater to set the basic authentication by -u [username]:[password]</li>
                        <li><common-icon type="_bulb" /> setup a http request head key: Authorization with the basic authen value</li>
                    </ul>
                    <ul>
                          <li><common-icon type="_bulb" /> add a http get request args with "api_key" and the basic authentication. </li>
                          <li><common-icon type="_bulb" /> e.g.  http://localhost/[REST API]?api_key=[username]:[password]</li>
                    </ul>
                  </TabPane>
                  <TabPane label="API Key Authentication" name="name2">
                    <ul>
                        <li><common-icon type="_bulb" /> add an API key authentication in the request head.</li>
                        <li><common-icon type="_bulb" /> Key name=X-{* app_name | capitalize *}-Api</li>
                        <li><common-icon type="_bulb" /> Key value=[The account's API Key]</li>
                        <li><common-icon type="_bulb" /> e.g. curl -H 'X-{* app_name | capitalize *}-Api:[API Key]' ......</li>
                    </ul>
                  </TabPane>
              </Tabs>

          </Card>
      </Col>
    </Row>
    <Row>
      <Col span="24">
          <ApidocCard :key="key"></ApidocCard>
      </Col>
    </Row>

  </Row>
</template>

<script>
import UserCard from './components/user-card'
import CommonIcon from '@/components/common-icon'
import ApidocCard from '@/view/components/apidoc-card'

export default {
  name: 'home',
  data () {
    return {
      refresh:true,
      key: this.$route.path,
      appVersion: this.$store.state.app.version,
    }
  },
  components: {
    UserCard,
    CommonIcon,
    ApidocCard
  },
  computed: {
    userName () {
      return this.$store.state.user.userName
    },
     userId () {
      return this.$store.state.user.userId
    },
    access () {
      return Array.from(this.$store.state.user.access)
    },
    loginName () {
      return this.$store.state.user.loginName
    }
  }
}
</script>

<style>
.welcome-message {
    font-size: 2em;
    color: #2d8cf0;
}
</style>
