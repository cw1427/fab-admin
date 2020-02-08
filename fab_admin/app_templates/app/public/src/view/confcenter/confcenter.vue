<template>
<div class="">
    <Row>
      <Col span="24">
        <Card style="">
          <template v-if="projects.length">  
            <Select v-model="projectSelect" multiple style="width:260px;" @on-change="filterProject" :filterable="true">
                <Option v-for="item in projects" :value="item" :key="item">{{ item }}</Option>
            </Select>
            <Tabs type="line" v-model="activePro">
              <template v-for="proj in showProjects">  
                    <TabPane :label="proj" icon="logo-apple" :name="proj">
                        <conf-table v-if="activePro==proj" :proj="activePro"></conf-table>
                    </TabPane>
              </template>
            </Tabs>
          </template>
          <template v-else>
              <Alert type="warning">You don't have any read permission on any projects  </Alert>
          </template>
        </Card>
      </Col>
    </Row>
</div>
</template>

<script>
import ConfTable from './components/conftable.vue'
import { Message,LoadingBar } from 'iview'
import {getProjects} from '@/api/confcenter'
export default {
  name: 'ConfCenter',
  data () {
      return {
          projects: [],
          projectSelect: [],
          activePro: '',
      }
  },
  components: {
      ConfTable
  },

  created() {
    this.loadProject();
  },
  computed: {
      showProjects(){
          if (this.projectSelect.length<=0) return this.projects;
          return this.projectSelect;
      }
  },
  methods: {
    loadProject () {
        //----axois search benchmark
        LoadingBar.start()
        this.loading=true
        getProjects().then( res => {
              const data = res.data
              if (res.status === 200) {
                  this.projects = data.data
                  this.activePro = this.projects[0]
              } else {
                  Message.error( (data.message == null)? 'Load failed': data.message )
              }
              LoadingBar.finish()
              this.loading=false
          }).catch( err => {
              Message.error(err.response.data.message)
              LoadingBar.error()
              this.loading=false
          })
    },
    filterProject(){
        if (this.projectSelect.length>0){
            this.activePro=null;
            this.$nextTick(() => {
                this.activePro = this.projectSelect[this.projectSelect.length-1];    
            });
            
        }else{
            this.activePro=null;
            this.$nextTick(() => {
                this.activePro = this.projects[0];
            }); 
        }
    }
  }
}
</script>

<style>

</style>
