<template>
<div class="">
    <Form ref="userInfoForm" :model="formItems" :label-width="200" :rules="formRules" :style="{width: '50%'}">
        <FormItem label="Login Name:" prop="loginName">
            <Input v-model="formItems.loginName" disabled></Input>
        </FormItem>
        <FormItem label="User Type:">
            <Input v-model="formItems.userType" disabled></Input>
        </FormItem>
        <FormItem label="Roles:">
            <template v-for="role in formItems.accesses">
                <Tag color="blue" type='border'>{{role}}</Tag>
            </template>
        </FormItem>
        <FormItem label="First Name:"  prop="firstName">
            <Input v-model="formItems.firstName" placeholder="First Name"></Input>
        </FormItem>
        <FormItem label="Last Name:" prop="lastName">
            <Input v-model="formItems.lastName" placeholder="Last Name"></Input>
        </FormItem>
        <FormItem label="Email" prop="email">
            <Input v-model="formItems.email" placeholder="Email"></Input>
        </FormItem>
        <FormItem>
            <Button type="primary" @click="handleSubmit">Submit</Button>
            <Button style="margin-left: 8px" @click="handleReset">Reset</Button>
        </FormItem>
    </Form>
</div>
</template>

<script>
import {isEmptyObject} from '@/libs/util'
import {selfUpdateUser} from '@/api/user'
import { mapMutations, mapActions } from 'vuex'
import { LoadingBar } from 'iview'
export default {
  name: 'BaseInfo',

  data() {
      return {
          formItems:{
            loginName: this.$store.state.user.loginName,
            firstName: this.$store.state.user.firstName,
            lastName: this.$store.state.user.lastName,
            email: this.$store.state.user.email,
            userType:  this.$store.state.user.userType,
            accesses:  this.$store.state.user.access,
          },
          formRules: {
             firstName:[{required: true, message: 'The name cannot be empty', trigger: 'blur'},
                {max: 20, min:3, trigger: 'blur'}],
             lastName:[{required: true, message: 'The name cannot be empty', trigger: 'blur'},
                {max: 20, min:3, trigger: 'blur'}],
             email: [{required: true, message: 'The name cannot be empty', trigger: 'blur'},
                   {type: 'email', message: 'Wrong email format', trigger: 'blur'}]
          }
      }
  },
  methods: {
      ...mapMutations([
          'setFirstName',
          'setLastName',
          'setEmail'
      ]),
      handleSubmit () {
                this.$refs['userInfoForm'].validate((valid) => {
                    if (valid) {
                        let params = {}
                        if (this.formItems.firstName != this.$store.state.user.firstName){
                            params.first_name=this.formItems.firstName
                        }
                        if (this.formItems.lastName != this.$store.state.user.lastName){
                            params.last_name=this.formItems.lastName
                        }
                        if (this.formItems.email != this.$store.state.user.email){
                            // this.$set(params,'last_name',this.formItems.lastName)
                            params.email = this.formItems.email
                        }
                        if (isEmptyObject(params)){
                            this.$Message.warning('There is no change')
                        }else{
                            LoadingBar.start()
                            selfUpdateUser(params).then(res => {
                                const data = res.data
                                if (res.status === 200) {
                                    LoadingBar.finish()
                                    this.$Message.success(data.msg)
                                    this.setFirstName(this.formItems.firstName)
                                    this.setLastName(this.formItems.lastName)
                                    this.setEmail(this.formItems.email)
                                } else {
                                    LoadingBar.error()
                                    this.$Message.error('Load user list failed')
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
      handleReset () {
        this.$refs['userInfoForm'].resetFields();
      }
  }
}
</script>

<style>

</style>
