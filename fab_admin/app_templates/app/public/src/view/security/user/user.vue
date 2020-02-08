<template>
<div>
  <Row type="flex">
    <Col span="24">
      <Card >
        <p slot="title">
            <Icon type="ios-people"></Icon>
            User List
        </p>

        <div slot="extra">
        </div>
        <div id="toolbar">
      	    <Button type="primary" icon="md-person-add" style="" @click="addShow">Add local user</Button>
            <Button type="info" icon="md-person-add" style="margin-left:2px" @click="pickLdapShow">Pick LDAP user</Button>
      	</div>
        <BootstrapTable  ref="bt"
            :columns="tableColumns"
            :options="options"
            @onPostBody="vueFormatterPostBody"
        />
      </Card>
      <Modal
          v-model="showInfo"
          title="User detail info"
          :draggable="true">
          <profile-form :items="pfitems"></profile-form>
          <div slot="footer">
              <Button type="primary" @click="showInfo=false">OK</Button>
          </div>
      </Modal>
      <Modal v-model="showAdd"
          :title="formItem.title"
          :mask-closable="false"
          :draggable="false" :width="600">

        <div class="">
            <Form ref="userAddForm" :model="formItem" :label-width="120" :rules="formRules">
                <FormItem label="First Name:"  prop="fn">
                    <Input v-model="formItem.fn" placeholder="First Name" :disabled="(targetRow && targetRow.extinfo.user_type ==='ldap') ? true : false "></Input>
                </FormItem>
                <FormItem label="Last Name:"  prop="ln">
                    <Input v-model="formItem.ln" placeholder="Last Name" :disabled="(targetRow && targetRow.extinfo.user_type ==='ldap') ? true : false "></Input>
                </FormItem>
                <FormItem label="Login Name:"  prop="un">
                    <Input v-model="formItem.un" placeholder="Login Name" :disabled="(targetRow && targetRow.extinfo.user_type ==='ldap') ? true : false "></Input>
                </FormItem>
                <FormItem label="Email:"  prop="email">
                    <Input v-model="formItem.email" placeholder="Email" :disabled="(targetRow && targetRow.extinfo.user_type ==='ldap') ? true : false "></Input>
                </FormItem>
                <FormItem label="Is Active?"  prop="active">
                  <RadioGroup v-model="formItem.active">
                    <Radio label="1">Active</Radio><Radio label="0">Locaked</Radio>
                  </RadioGroup>
                </FormItem>
                <FormItem label="Role:"  prop="">
                    <Select v-model="formItem.rolesSelect" multiple style="width:260px;">
                        <Option v-for="item in roles" :value="item.id" :key="item.id">{{ item.name }}</Option>
                    </Select>
                </FormItem>
                <template v-if="isAllowSetPwd">
                  <FormItem label="Password:"  prop="password" :required="targetRow?false:true">
                      <vue-password v-model="formItem.password" @blur="handlePasswordBlur"
                          classes="input">
                      </vue-password>
                  </FormItem>
                  <FormItem label="Confirm Password:"  prop="confirmPassword" :required="targetRow?false:true">
                      <vue-password v-model="formItem.confirmPassword" @blur="handleConfirmPasswordBlur"
                          classes="input">
                      </vue-password>
                  </FormItem>
                </template>
            </Form>
        </div>

          <div slot="footer">
              <Button type="primary" @click="handleSubmit" ref="submitBtn">Submit</Button>
              <Button @click="showAdd=false">Cancel</Button>
          </div>
      </Modal>

      <Modal
          v-model="showPickLdapUser"
          :mask-closable="false"
          title="Pickup LDAP users into system"
          :draggable="false" :width="600">
          <Form ref="ldapForm" :model="ldapFormItem" :label-width="120" :rules="ldapFormRules">
                <FormItem label="moto coreId:"  prop="coreId">
                    <Input style="width:260px;" type="textarea" :autosize="{minRows: 5,maxRows: 10}" v-model="ldapFormItem.coreId" placeholder="Enter coreIds one per line"></Input>
                </FormItem>
                <FormItem label="Role:"  prop="">
                    <Select v-model="ldapFormItem.rolesSelect" multiple style="width:260px;">
                        <Option v-for="item in roles" :value="item.id" :key="item.id">{{ item.name }}</Option>
                    </Select>
                </FormItem>
        </Form>

          <div slot="footer">
              <Button type="primary" @click="handlePickLdapUserSubmit" ref="submitBtn">Submit</Button>
              <Button @click="showPickLdapUser=false">Cancel</Button>
          </div>
      </Modal>

    </Col>
  </Row>
</div>
</template>
<script>
import {getUserList,deleteUserById,updateUserById,addUser,editUser,syncLdapUser} from '@/api/user'
import { Message,Spin,LoadingBar } from 'iview'
import ProfileForm from '@/view/components/profile-form'
import mixin from '_c/common/btMixin.js'
import baseURL from '_conf/url'
import VuePassword from 'vue-password'
import { mapActions } from 'vuex'

const userStatus = {
    2: {
      value: 0,
      name: 'All'
    },
    0: {
      value: 2,
      name: 'Locked',
      color: 'red'
    },
    1: {
      value: 1,
      name: 'Actived',
      color: 'green'
    },
  };
export default {
  name: 'User',
  mixins: [mixin],
  components: {
    ProfileForm,
    VuePassword
  },
  data () {
    const validatePassCheck = (rule, value, callback) => {
                        if ((this.formItem.password !=null && this.formItem.password !=='') && (value==null || value === '')) {
                            callback(new Error('Please enter your password again'));
                        } else if (value !== this.formItem.password) {
                            callback(new Error('The two input passwords do not match!'));
                        } else {
                            callback();
                        }
        };
    return {
      //roles: this.$store.state.user.allRoles,
      pfitems: [{name:'name1',value:'value1'}],
      showAdd: false,
      showInfo: false,
      showPickLdapUser: false,
      tableColumns: [
          {
            title: 'id',
            field: 'id',
            visible: false
          },
          {
            title: 'Login Name',
            field: 'loginname',
          },
          {
            title: 'User Name',
            field: 'username',
          },
        {
            title: 'Realm Type',
            field: 'user_type',
          },
          {
            title: 'Roles',
            field: 'roles',
          },
          {
            title: 'Email',
            field: 'email',
          },
          {
            title: 'Last Login',
            field: 'lastlogin',
          },
          {
            title: 'Active',
            field: 'status',
            width: 80,
            formatter: (value,row) => {
              const _status = {
                '1': {
                  value: 1,
                  name: 'Active',
                  color: 'green'
                },
                '0': {
                  value: 0,
                  name: 'Locked',
                  color: 'red'
                },
              };

              return this.vueFormatter({
                 template: '<Tag :color="sc">{{status}}</Tag>',
                 data() {
                   return {
                      sc: this._formatStatus(value, _status).color,
                      status: this._formatStatus(value, _status).name
                   }
                 },
                methods: {
                   _formatStatus: (v,s)=>{
                     return this.formatStatus(v,s)
                   }
                 }
              })
            }
          },
          {
            title: "Actions",
            field: "action",
            width: 180,
            formatter: (value,row) => {
              return this.vueFormatter({
                 template: `<div>
                            <Tooltip placement="top" content="Edit" v-if="extinfo">
                                <Button icon="ios-color-wand" size="small" type="success" @click="_edit_click"></Button>
                            </Tooltip>
                            <Tooltip placement="top" content="Detail">
                                <Button icon="ios-search" size="small" type="primary" @click="_info_click"></Button>
                            </Tooltip>
                            <Tooltip placement="top" content="Delete">
                              <Poptip title="Confirm delete?"  :confirm="true" :transfer="true" @on-ok="_deleteClick">
                                <Button icon="ios-trash" size="small" type="error"></Button>
                              </Poptip>
                            </Tooltip>
                        </div>`,
                 data() {
                   return {
                      extinfo: row.extinfo ? row.extinfo : null
                   }
                 },
                 props:[
                 ],
                 methods: {
                   _edit_click: ()=>{
                     this.editShow(row)
                   },
                   _info_click: ()=>{
                     this.infoShow(row)
                   },
                   _deleteClick: ()=>{
                      this.handleDelete(row.id)
                   }
                 }
              })
            }
          }
        ],
      options: {
          showColumns: true,
          showRefresh: true,
          search: true,
          url: baseURL + 'api/user_list',
          ajaxOptions: {
            xhrFields: {
                withCredentials: true
            }
          },
          sidePagination: "server",
          pagination: true,
          pageSize: 10,
          pageNumber: 1,
          pageList:[10,20,50,100],
          smartDisplay: false,
          toolbar: '#toolbar'
      },
      formItem: {
                id: null,
                title: 'Add user',
                editable: false,
                password: '',
                confirmPassword: '',
                fn: null,
                ln: null,
                un: null,
                email: null,
                active: '1',
                rolesSelect: [],
      },
      formRulesAdd: {
          fn:[{required: true, message: 'The first name cannot be empty', trigger: 'blur'},
              {max: 20, min:3, trigger: 'blur'}],
          ln:[{required: true, message: 'The last name cannot be empty', trigger: 'blur'}],
          un:[{required: true, message: 'The login name cannot be empty', trigger: 'blur'}],
          email:[{required: true, message: 'The email cannot be empty', trigger: 'blur'}],
          password: [{required: true, message: 'The password cannot be empty', trigger: 'blur'},
                {max: 200, min:6, trigger: 'blur'}],
          confirmPassword: [{required: true, message: 'The password cannot be empty', trigger: 'blur'},
                {max: 200, min:6, trigger: 'blur'},{validator: validatePassCheck,trigger: 'blur'}],
      },
      formRulesEdit: {
          fn:[{required: true, message: 'The first name cannot be empty', trigger: 'blur'},
              {max: 20, min:3, trigger: 'blur'}],
          ln:[{required: true, message: 'The last name cannot be empty', trigger: 'blur'}],
          un:[{required: true, message: 'The login name cannot be empty', trigger: 'blur'}],
          email:[{required: true, message: 'The email cannot be empty', trigger: 'blur'}],
          password: [{required: false, message: 'The password cannot be empty', trigger: 'blur'},
                {max: 200, min:6, trigger: 'blur'}],
          confirmPassword: [{required: false, message: 'The password cannot be empty', trigger: 'blur'},
                {max: 200, min:6, trigger: 'blur'},{validator: validatePassCheck,trigger: 'blur'}],
      },
      targetRow: null,
      ldapFormItem: {
        coreId:null,
        rolesSelect:null
      },
      ldapFormRules: {
          coreId:[{required: true, message: 'Ther coreIds must not be empty', trigger: 'blur'}],
      }
    }// end of data return
  }, // end of data()
  created() {
    this.getAllRoles()
  },
  methods: {
    ...mapActions([
          'getAllRoles',
    ]),
    addShow(){
      this.targetRow = null
      this.handleReset()
      this.formItem.title='Add a new local user'
      this.formItem.editable= false
      this.formItem.fn=null
      this.formItem.ln=null
      this.formItem.un=null
      this.formItem.email=null
      this.formItem.active='1'
      this.formItem.rolesSelect=null
      this.showAdd = true
    },
    editShow(row){
      this.targetRow = row
      this.handleReset()
      this.formItem.title='Edit this user'
      this.formItem.id=row.id
      this.formItem.editable= true
      this.formItem.fn=row.username.split(' ')[0]
      this.formItem.ln=row.username.split(' ')[1]
      this.formItem.un=row.loginname
      this.formItem.email=row.email
      this.formItem.active=row.status.toString()
      this.formItem.rolesSelect=row.roles_id
      this.formItem.password=''
      this.showAdd = true
    },
    infoShow(row){
      let items= []
      for (let index in this.tableColumns){
        let i = {}
        let c=this.tableColumns[index]
        if (row[c.field] != null){
          this.$set(i,'name',c.title)
          this.$set(i,'value',row[c.field])
          items.push(i)
        }
      }
      this.pfitems = items
      this.showInfo=true
    },
    handleSubmit(){
      this.$refs['userAddForm'].validate((valid) => {
          if (valid) {
                  LoadingBar.start()
                  if (!this.formItem.editable){//----for add submit
                      addUser(this.formItem).then(res => {
                          const data = res.data
                          if (res.status === 200) {
                              LoadingBar.finish()
                              this.$Message.success(data.msg)
                              this.showAdd = false
                              this.$refs['bt'].refresh()
                          } else {
                              LoadingBar.error()
                              this.$Message.error( (data.msg == null)? 'Add user failed' : data.msg)
                          }
                      }).catch( err => {
                          LoadingBar.error()
                          this.$Message.error(err.response.status)
                          console.log(err.response.data)
                      })
                  }else{
                    editUser(this.formItem).then(res => {
                          const data = res.data
                          if (res.status === 200) {
                              LoadingBar.finish()
                              this.$Message.success(data.msg)
                              this.showAdd = false
                              this.$refs['bt'].refresh()
                          } else {
                              LoadingBar.error()
                              this.$Message.error( (data.msg == null)? 'Edit user failed' : data.msg)
                          }
                      }).catch( err => {
                          LoadingBar.error()
                          this.$Message.error(err.response.status)
                          console.log(err.response.data)
                      })
                  }
          } else {
              this.$Message.error('Validation Failed!');
          }
      })
    },
    handleDelete(id){
      let data = {
          token:this.$store.state.user.token,
          id
      }
      deleteUserById(data).then( res => {
          const data = res.data
          if (res.status === 200) {
            Message.success(data.msg)
            this.$refs['bt'].refresh()
          } else {
              Message.error('Delete user failed')
          }
      }).catch( err => {
          Message.error(err.response.status)
          console.log(err.response.data)
      })
    },
    formatStatus(value, status) {
        return status[value] || {value: '', name: ''}
    },
     handlePasswordBlur(value) {
        this.$refs['userAddForm'].validateField('password')
    },
    handleConfirmPasswordBlur(value) {
        this.$refs['userAddForm'].validateField('confirmPassword')
    },
    handleReset () {
        this.$refs['userAddForm'].resetFields();
    },
    pickLdapShow(){
        this.$refs['ldapForm'].resetFields();
        this.ldapFormItem.coreId=null
        this.ldapFormItem.rolesSelect=null
        this.showPickLdapUser=true
    },
    handlePickLdapUserSubmit(){
      this.$refs['ldapForm'].validate((valid) => {
          if (valid) {
                  LoadingBar.start()
                  syncLdapUser(this.ldapFormItem).then(res => {
                      const data = res.data
                      if (res.status === 200) {
                          LoadingBar.finish()
                          this.$Message.success("success added: " + data.success_list)
                          if (data.failed_list.length>0){
                              this.$Message.error("Failed added: " + data.failed_list)
                          }
                          this.showPickLdapUser = false
                          this.$refs['bt'].refresh()
                      } else {
                          LoadingBar.error()
                          this.$Message.error( (data.msg == null)? 'Add user failed' : data.msg)
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
    }
  },
  computed: {
     roles() {
         return this.$store.state.user.allRoles
     },
     isAllowSetPwd(){
       return !(this.targetRow && this.targetRow.extinfo.user_type ==='ldap')
     },
     formRules(){
       return  (this.targetRow==null) ? this.formRulesAdd : this.formRulesEdit
     }

  }

}
</script>
<style>

</style>
