<template>
<div>
    <Row type="flex" style="padding-bottom:5px">
        <Col span="3">
            <Button type="primary" v-on:click="addShow">Add a new config item</Button>
        </Col>
    </Row>
    <Row type="flex">
      <Col span="24">
            <!--<filter-table @load="loadData"
                        :loading="loading"
                        :data="configs"
                        :columns="tableColumns"
                        :search="search"
                        v-if="refresh"
                        :showRowNum="showRowNum">
            </filter-table>-->
             <Table
                :loading="loading"
                :show-header="true"
                :highlight-row="true"
                :border="true"
                :data="configs"
                :columns="tableColumns"
                v-if="refresh"
                :showRowNum="true"
                stripe>
            </Table>
        </Col>
    </Row>

<Modal
          v-model="showInfo"
          title="Property history info"
          :draggable="false">
          <profile-form :items="pfitems"></profile-form>
          <div slot="footer">
              <Button type="primary" @click="showInfo=false">OK</Button>
          </div>
  </Modal>
  <Modal v-model="showAdd"
          :title="formItem.title"
          :mask-closable="false"
          :draggable="false" :width="1000">

        <div class="">
            <Form ref="confAddForm" :model="formItem" :label-width="120" :rules="formRules">
                <FormItem label="Config Name:"  prop="name">
                    <Input v-model="formItem.name" placeholder="Enter something..." :disabled="formItem.editable"></Input>
                </FormItem>
                <FormItem label=""  prop="">
                    <RadioGroup v-model="formItem.valueType">
                        <Radio label="tag"></Radio><Radio label="json"></Radio><Radio label="text"></Radio>
                    </RadioGroup>
                </FormItem>
                <FormItem label="Config Value"  prop="value">
                    <Row v-if="isValueTypeJson">
                        <Col span="12">
                            <v-jsoneditor  v-model="valueJson" :options="jeEptions" :plus="false" height="400px" @error="onJsonError"></v-jsoneditor>
                        </Col>
                        <Col span="12">
                            <v-jsoneditor  v-model="valueJson" :options="jeEptionsCode" :plus="false" height="400px" @error="onJsonError"></v-jsoneditor>
                        </Col>
                    </Row>
                    <input-tag v-if="isValueTypeTag" v-model="valueTag" placeholder="Input value,press Enter to add a new item" :add-tag-on-keys="tagDelimiter"></input-tag>
                    <Input v-if="isValueTypeText" v-model="formItem.value" type="textarea" :autosize="{minRows: 10,maxRows: 30}" placeholder="Json format string or plain string"></Input>
                </FormItem>
            </Form>
        </div>

          <div slot="footer">
              <Button type="primary" @click="handleSubmit" ref="submitBtn">Submit</Button>
              <Button @click="showAdd=false">Cancel</Button>
          </div>
  </Modal>
</div>
</template>

<script>
import ProfileForm from '@/view/components/profile-form'
import FilterTable from '@/view/components/filter-table'
import {getConfigs, addOrEditConfig, deleteConfItem} from '#/confcenter/public/viewui/api.js'
import { Message,LoadingBar,Table } from 'iview'
import {getDate,isJSON} from '@/libs/tools'
import VueJsonPretty from 'vue-json-pretty'
import VJsoneditor from 'v-jsoneditor'
import InputTag from 'vue-input-tag'
export default {
  name: 'ConfTable',
  props:  [
      'proj',
    ],
  components: {
    FilterTable,
    ProfileForm,
    VueJsonPretty,
    VJsoneditor,
    InputTag
  },
  data () {
    return {
            search: {},
            showInfo:false,
            showAdd:false,
            showRowNum:true,
            pfitems:[],
            configs: [],
            loading:false,
            formItem: {
                title: 'Add a new config',
                editable: false,
                name: '',
                value: '',
                type: '',
                valueType: 'tag'
            },
            formRules: {
                name:[{required: true, message: 'The name cannot be empty', trigger: 'blur'},
                    {max: 20, min:3, trigger: 'blur'}],
                value:[{required: true, message: 'The value cannot be empty', trigger: 'blur'}]
            },
            tableColumns: [
                {
                    type: 'index',
                    width: 50
                },
                {
                    title: 'name',
                    key: 'name',
                    sortable: false,
                    width: 120
                },
                {
                    title: 'value',
                    key: 'value',
                    maxWidth: 700,
                    minWidth: 300,
                    render: (h,params) => {
                        if (typeof(params.row.value) === 'string' || params.row.value instanceof String){
                            let lines = params.row.value.split(/\r?\n/);
                            let domLines =[];
                            lines.forEach(function(element) {
                                if (element !== null && element !==''){
                                    let domLine = h('Alert',{},element);
                                    domLines.push(domLine);
                                }
                            });
                            return h('div',{},domLines);
                        }else{
                            return h('VueJsonPretty',{
                                props:{
                                    data:params.row.value,
                                    deep: 2,
                                    showLength:true
                                }
                            });
                        }
                    }
                },
                {
                    title: 'changed by',
                    key: 'changed_by',
                },
                {
                    title: 'changed on',
                    key: 'changed_on',
                    render: (h,params) => {
                        let dateString = getDate(params.row.changed_on,'year')
                        return h('div',{},dateString)
                    }
                },
                {
                    title: 'Operation',
                    key: 'action',
                    width: 180,
                    align:'center',
                    render: (h,params) => {
                        return h('div',[
                            h('tooltip',{
                                props: {
                                    content: 'Edit',
                                    placement: 'top'
                                }
                            }, [h('Button', {
                            props: {
                                icon: 'ios-color-wand',
                                size: 'small',
                                type: 'success',
                                ghost: true
                            },
                            style: {
                                marginRight: '1px'
                            },
                            on: {
                                click:  () => {
                                this.editShow(params.row);
                                }
                            }
                            }, '')]),
                            h('tooltip',{
                                props: {
                                    content: 'Detail',
                                    placement: 'top'
                                }
                            },[h('Button', {
                            props: {
                                type: 'primary',
                                size: 'small',
                                icon: 'ios-search'
                            },
                            style: {
                                marginRight: '1px'
                            },
                            on: {
                                click:  () => {
                                this.infoShow(params.row);
                                }
                            }
                            }, '')]),
                            h('tooltip',{
                                props: {
                                    content: 'History',
                                    placement: 'top'
                                }
                            },[h('Button', {
                            props: {
                                type: 'warning',
                                size: 'small',
                                icon: 'ios-albums'
                            },
                            style: {
                                marginRight: '1px'
                            },
                            on: {
                                click:  () => {
                                this.infoShow(params.row);
                                }
                            }
                            }, '')]),
                            h('tooltip',{
                                props: {
                                    content: 'Delete',
                                    placement: 'top'
                                }
                            },[h('Poptip', {
                            props: {
                                confirm: true,
                                title: 'Confirm delete?',
                                transfer:true
                            },
                            on: {
                                'on-ok': () => {
                                this.handleDelete(params)
                                //vm.$emit('on-delete', params)
                                }
                            }
                            },[h('Button', {
                                props: {
                                    type: 'error',
                                    size: 'small',
                                    icon: 'ios-trash',
                                    placement: 'top'
                                },
                                style: {
                                marginRight: '1px'
                                }
                                }, ''
                                )]
                            )
                        ])])
                    }
                }
            ],
            jeEptions:{mode:'tree'},
            jeEptionsCode:{mode:'code'},
            tagDelimiter:[13]
      }
  },
  created() {
    this.loadData();
  },
  methods: {
        loadData () {
            //----axois search configs
            LoadingBar.start()
            this.loading=true
            getConfigs(this.proj).then( res => {
                const data = res.data
                if (res.status === 200) {
                    this.configs = data.data
                } else {
                    Message.error('Load failed')
                }
                LoadingBar.finish()
                this.loading=false
            }).catch( err => {
                Message.error(err.response.status)
                console.log(err.response.data)
                LoadingBar.error()
                this.loading=false
            })
        },
        infoShow(row){
            let items= []
            for (let index in this.tableColumns){
                let i = {}
                let c=this.tableColumns[index]
                if (row[c.key] != null){
                this.$set(i,'name',c.key)
                if (c.key === 'create_on' || c.key === 'changed_on'){
                    this.$set(i,'value',getDate(row[c.key],'year'))
                }else{
                    this.$set(i,'value',row[c.key])
                }
                items.push(i)
                }
            }
            this.pfitems = items
            this.showInfo=true
        },
        addShow(){
            this.formItem.title='Add a new config'
            this.formItem.editable= false
            this.formItem.name=''
            this.formItem.value=''
            this.formItem.valueType='tag'
            this.formItem.type=''
            this.handleReset()
            this.showAdd = true
        },
        editShow(row){
            this.formItem.title = 'Edit a config'
            this.formItem.editable= true
            this.formItem.name = row['name']
            this.formItem.value = (typeof(row['value'])==='object')? JSON.stringify(row['value']) : row['value']
            this.formItem.valueType='tag'
            this.showAdd=true
        },
        handleSubmit () {
                this.$refs['confAddForm'].validate((valid) => {
                    if (valid) {
                            let params = {
                                proj:this.proj,
                                name: this.formItem.name,
                                value:this.formItem.value,
                                editable:this.formItem.editable
                            }
                            LoadingBar.start()
                            addOrEditConfig(params).then(res => {
                                const data = res.data
                                if (res.status === 200) {
                                    LoadingBar.finish()
                                    this.$Message.success(data.message)
                                    this.showAdd = false
                                    this.loadData()
                                } else {
                                    LoadingBar.error()
                                    this.$Message.error( (data.message == null)? 'update config failed' : data.message)
                                }
                            }).catch( err => {
                                LoadingBar.error()
                                this.$Message.error(err.response.status)
                                console.log(err.response.data)
                            })
                    } else {
                        this.$Message.error('Validation Failed!');
                    }
                })
            },
        handleReset () {
                this.$refs['confAddForm'].resetFields();
        },
        handleDelete(params){
            let data = {
                proj: this.proj,
                name:params.row.name
            }
            deleteConfItem(data).then( res => {
                const data = res.data
                if (res.status === 200) {
                    this.configs.splice(params.index,1)
                } else {
                    Message.error( (data.message == null)? 'Delete config failed': data.message )
                }
            }).catch( err => {
                Message.error(err.response.status)
                console.log(err.response.data)
            })
        },
        onJsonError(){
            this.$refs['submitBtn'].disabled=true;
        }
  },
  computed: {
    refresh(){
        return this.configs != null ? true:false
     },
    isValueTypeJson(){
        return this.formItem.valueType=='json';
    },
    isValueTypeTag(){
        return this.formItem.valueType=='tag';
    },
    isValueTypeText(){
        return this.formItem.valueType=='text';
    },
    valueJson: {
        get: function(){
            if (this.formItem.value instanceof Object){
                return  this.formItem.value;
            } else{
                    try {
                        return JSON.parse(this.formItem.value);
                    } catch (e) {
                        return this.formItem.value;
                    }
            }
        },
        set: function(newValue) {
            this.$refs['submitBtn'].disabled=false;
            this.formItem.value = (newValue instanceof Object)? JSON.stringify(newValue) : newValue;
        }
    },
    valueTag: {
        get: function(){
            if (this.formItem.value=='') return [];
            if (typeof(this.formItem.value) === 'string' || this.formItem.value instanceof String){
                return this.formItem.value.split(/\r?\n/);
            }else{
                if (typeof(this.formItem.value) instanceof Array){
                    return this.formItem.value;
                }else{
                    return [this.formItem.value];
                }
            }
        },
        set: function(newValue) {
            this.formItem.value = (newValue instanceof Array)? newValue.join("\n") : newValue;
        }
    }
  }
}
</script>

<style>
</style>
