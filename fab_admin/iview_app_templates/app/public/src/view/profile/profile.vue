<template>
<div class="">
    <Row>
      <Col span="24">
        <Card style="">
          <Tabs type="line">
              <TabPane label="Basic Info" icon="logo-apple">
                <base-info />
              </TabPane>
          </Tabs>
          <Tabs type="line" class="" v-if="this.$store.state.user.userType=='local'" >
              <TabPane label="Password" icon="logo-apple">
                <password />
              </TabPane>
          </Tabs>
          <Tabs type="line" class="">
              <TabPane label="Api Key" icon="logo-apple">
                <apikey />
              </TabPane>
          </Tabs>
        </Card>
      </Col>
    </Row>
</div>
</template>

<script>

import BaseInfo from './components/baseinfo'
import Password from './components/password'
import Apikey from './components/apikey'
export default {
  name: 'Profile',
  components: {
    BaseInfo,
    Password,
    Apikey
  },
  computed: {

  }
}
</script>

<style>

</style>
