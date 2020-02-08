<template>
<div class="">
    <Row>
      <Col span="12">
            <label >Reader group </label>
            <Transfer
                filterable
                :data="allUsers"
                :target-keys="targetReader"
                :render-format="renderFormat"
                @on-change="handleReaderTransfer">
            </Transfer>
            <div style="margin-top:10px">
              <Button type="primary" @click="handleSave('read')" >Save</Button>
              <Button @click="handleReset('read')" > Reset</Button>
            </div>    
      </Col>
      <Col span="12">
            <label >Writer group </label>
            <Transfer
                filterable
                :data="allUsers"
                :target-keys="targetWriter"
                :render-format="renderFormat"
                @on-change="handleWriterTransfer">
            </Transfer>
            <div style="margin-top:10px">
              <Button type="primary" @click="handleSave('write')" >Save</Button>
              <Button @click="handleReset('write')" > Reset</Button>
            </div>   
      </Col>
    </Row>
</div>
</template>

<script>
import { Message,LoadingBar } from 'iview'
import {getProjPerm,updateProjPerm} from '@/api/confcenter'

export default {
  name: 'ConfPerm',
  data () {
      return {
          projects: [],
          activePro: '',
          targetReader: [],
          orgReader:[],
          targetWriter: [],
          orgWriter:[]
      }
  },
  components: {
      
  },
  props:  [
      'proj',//columns description Obj
  ],
  created() {
    this.loadPerm();
  },
  computed: {
      allUsers() {
          let allUsers = []
          this.$store.state.user.allUsers.forEach(element => {
                let temp = {}
                temp.key = element.username
                temp.value = element.first_name + ' ' + element.last_name
                allUsers.push(temp)
            });
          return allUsers
      }
  },
  methods: {
    loadPerm () {
        LoadingBar.start()
        getProjPerm(this.proj).then( res => {
            const data = res.data
            if (res.status === 200) {
                this.targetReader = data.reader
                this.orgReader = data.reader
                this.targetWriter = data.writer
                this.orgWriter = data.writer
            } else {
                Message.error( (data.message == null)? 'Load permission failed': data.message )
                LoadingBar.error()
            }
            LoadingBar.finish()
        }).catch( err => {
            Message.error(err.response.status)
            console.log(err.response.data)
        })
    },
    renderFormat(item){
        return item.value
    },
    handleReaderTransfer(newTargetKeys) {
        this.targetReader = newTargetKeys
    },
    handleWriterTransfer(newTargetKeys) {
        this.targetWriter = newTargetKeys
    },
    handleSave(perm) {
        LoadingBar.start()
        let params = {
            proj:this.proj,
            perm,
            users: (perm === 'read') ? this.targetReader : this.targetWriter
        }
        updateProjPerm(params).then( res => {
            const data = res.data
            if (res.status === 200) {
                Message.success(data.message)
            } else {
                Message.error( (data.message == null)? 'Update project perm failed': data.message)
                LoadingBar.error()
            }
            LoadingBar.finish()
        }).catch( err => {
            Message.error(err.response.status)
            console.log(err.response.data)
        })
    },
    handleReset(perm) {
        if (perm === 'read'){
            this.targetReader = this.orgReader
        }else{
            this.targetWriter = this.orgWriter
        }
    }
    
  }
}
</script>

<style>
</style>
