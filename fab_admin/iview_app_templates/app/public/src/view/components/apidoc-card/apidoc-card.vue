<template>
<Card style="">
    <p slot="title">
        <Icon type="ios-film-outline"></Icon>
        RESTAPI - {{docGroup}}
    </p>
    <div slot="extra">
          <RadioGroup v-model="docGroup" type="button" @on-change="handleDocGroupChange">
            <Radio label="all" ></Radio>
            <Radio label="Sample">Sample</Radio>
            <Radio label="Confcenter">Confcenter</Radio>
        </RadioGroup>
    </div>
    <Scroll height="530">
        <Collapse accordion>
            <template v-for="(doc,index) in endPoints">
                <Panel :name="`endpoint_${index}`">
                    API: {{ doc.rule | url_filter(baseURL)}}
                    <div slot="content">
                        <Collapse accordion>
                            <Panel :name="`desc_${index}`">
                                Request Description
                                <div slot="content">
                                    <Tabs type="line">
                                        <TabPane label="Description">
                                            <div v-html="doc.docstring_json.desc"></div>
                                        </TabPane>
                                        <TabPane label="Media Type">
                                            {{doc.docstring_json.mediaType}}
                                        </TabPane>
                                        <TabPane label="Json data request or response">
                                            {{doc.docstring_json.data}}
                                        </TabPane>
                                    </Tabs>
                                </div>
                            </Panel>
                            <Panel :name="`method_${index}`">
                                Request Methods
                                <p slot="content">
                                    <ul>
                                    <template v-for="m in doc.methods">
                                    <li> {{m}}</li>
                                    </template>
                                    </ul>
                                </p>
                            </Panel>
                            <Panel :name="`args_${index}`">
                                Request args
                                <p slot="content">
                                    <ul>
                                    <template v-for="m in doc.args">
                                    <li> {{m}}</li>
                                    </template>
                                    </ul>
                                </p>
                            </Panel>
                        </Collapse>
                    </div>
                </Panel>
            </template>
        </Collapse>
    </Scroll>
</Card>
</template>

<script>
import {getAutoDoc} from '@/api/user'
import { Message,Spin,LoadingBar } from 'iview'
import baseURL from '_conf/url'
export default {
  name: 'ApidocCard',
  components: {
  },
  data () {
    return {
        endPoints: [],
        baseURL,
        docGroup:'all'
    }
  },
  created() {
      this.loadData();
  },
  methods: {
    loadData () {
        //----axois search benchmark
        LoadingBar.start()
        let params={'group':this.docGroup}
        getAutoDoc(params).then( res => {
              const data = res.data
              if (res.status === 200) {
                  this.endPoints = data.data
              } else {
                  Message.error('Load failed')
              }
              LoadingBar.finish()
          }).catch( err => {
              Message.error(err.response.status)
              console.log(err.response.data)
              LoadingBar.error()
          })
    },
    handleDocGroupChange(value){
        this.loadData()
    }
  },
  filters: {
      url_filter(value,baseURL) {
          return baseURL.slice(0,baseURL.length-1) + value;
          //return this.baseURL + value
      }
  }
}
</script>

<style lang="less">

</style>
