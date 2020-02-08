<template>
<div class="">
    <Row type="flex">
        <Col span="2"></Col>
        <Col span="18">
            <Form ref="apikeyForm" inline :model="formItems">
                <FormItem>
                    <Button type="primary" @click="handleGen">
                        <template v-if="this.$store.state.user.apiKey">
                            Regenerate
                        </template>
                        <template v-else>Generate</template>
                    </Button>
                </FormItem>
                <FormItem prop="password" :style="{width: '72%'}">
                    <vue-password v-model="formItems.apikey" :disableStrength="true"
                            classes="input">
                    </vue-password>
                </FormItem>
            </Form>
        </col>
    </Row>
</div>
</template>

<script>
import VuePassword from 'vue-password'
import {genApikey} from '@/api/user'
import { LoadingBar } from 'iview'
import { mapMutations, mapActions } from 'vuex'
export default {
  name: 'Apikey',
  components: {
      VuePassword
  },
  data() {
      return {
          formItems: {
              apikey: this.$store.state.user.apiKey
          }
      }
  },
  methods: {
      ...mapMutations([
          'setApiKey'
      ]),
      handleGen(){
            LoadingBar.start()
            genApikey().then(res => {
                const data = res.data
                if (res.status === 200) {
                    LoadingBar.finish()
                    this.$Message.success(data.msg)
                    this.setApiKey(data.apikey)
                    this.formItems.apikey=data.apikey
                } else {
                    this.$Message.error('Genereate Apikey failed')
                    LoadingBar.error()
                }
            }).catch( err => {
                LoadingBar.error()
                this.$Message.error(err.response.status)
                console.log(err.response.data)
            })
      }
  }
}
</script>

<style>

</style>
