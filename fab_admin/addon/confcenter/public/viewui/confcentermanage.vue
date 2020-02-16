<template>
<div class="">
    <Row>
      <Col span="24">
        <Card style="">
          <Button @click="handleAddProj" type="primary" icon="ios-film-outline" style="margin-bottom:2px">Add a new config project</Button>
          <Poptip confirm title="Confirm to delete this project" @on-ok="handleDelProj">
               <Button type="error" icon="ios-film-outline" style="margin-bottom:2px">Delete current config project</Button>
          </Poptip>
          <template v-if="projects.length">
            <Select v-model="projectSelect" multiple style="width:260px;" @on-change="filterProject" :filterable="true">
                <Option v-for="item in projects" :value="item" :key="item">{{ item }}</Option>
            </Select>
            <Tabs type="line" v-model="activePro">
              <template v-for="proj in showProjects">
                    <TabPane :label="proj" icon="logo-apple" :name="proj">
                     <conf-perm v-if="activePro==proj" :proj="activePro"></conf-perm>
                    </TabPane>
              </template>
            </Tabs>
          </template>
          <template v-else>
              <Alert type="warning">You don't have any Write permission on any projects  </Alert>
          </template>
        </Card>
      </Col>
    </Row>
</div>
</template>

<script>
import { Message,LoadingBar } from 'iview'
import {getProjects,addProject, deleteConfProj} from '#/confcenter/public/viewui/api.js'
import ConfPerm from './components/confperm.vue'
import { mapActions } from 'vuex'

export default {
  name: 'ConfCenterManage',
  data () {
      return {
          projects: [],
          projectSelect: [],
          activePro: '',
          newProj: ''
      }
  },
  components: {
      ConfPerm
  },

  created() {
    this.loadProject()
    this.getAllUsers()
  },
  computed: {
    refresh(){
        return this.projects != null ? true:false
     },
    showProjects(){
          if (this.projectSelect.length<=0) return this.projects;
          return this.projectSelect;
    }
  },
  methods: {
    ...mapActions([
          'getAllUsers',
    ]),
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
                  Message.error(data.message)
              }
              LoadingBar.finish()
              this.loading=false
          }).catch( err => {
              Message.error(err.response.status)
              LoadingBar.error()
              this.loading=false
          })
    },
    handleAddProj() {
          this.$Modal.confirm({
              title: '<div style="padding-bottom:5px">Project name</div>',
              render: (h) => {
                        return h('Input', {
                            props: {
                                value: this.newProj,
                                autofocus: true,
                                placeholder: 'Please enter your name...'
                            },
                            on:{
                                input :(val) => {
                                    this.newProj = val
                                }
                            }
                        })
                    },
                onOk: () => {
                        if (this.newProj==''){
                            this.$Message.warning('project name should not be empty')
                        }else{
                            LoadingBar.start()
                            addProject(this.newProj.trim()).then( res => {
                                const data = res.data
                                if (res.status === 200) {
                                    Message.success(data.message)
                                    this.projects.push(this.newProj.trim())
                                } else {
                                    Message.error( (data.message == null)? 'Add project failed': data.message )
                                }
                                LoadingBar.finish()
                            }).catch( err => {
                                Message.error(err)
                                LoadingBar.error()
                            })
                        }
                    },
                onCancel: () => {
                        this.newProj=''
                    }
          });
    },//----end of handleAddProj
    handleDelProj(){
            let data = {
                proj: this.activePro
            }
            deleteConfProj(data).then( res => {
                const data = res.data
                if (res.status === 200) {
                    let index = this.projects.indexOf(this.activePro);
                    this.projects.splice(index,1);
                    this.activePro = this.projects[0];
                } else {
                    Message.error( (data.message == null)? 'Delete project failed': data.message )
                }
            }).catch( err => {
                Message.error(err.response.status)
                console.log(err.response.data)
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
