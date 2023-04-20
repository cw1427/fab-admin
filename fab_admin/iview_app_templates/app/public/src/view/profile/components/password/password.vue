<template>
<div class="">
    <Form ref="passwordForm" :model="formItems" :label-width="200" :rules="formRules" :style="{width: '70%'}">
        <FormItem label="New Password:" prop="password">
            <vue-password v-model="formItems.password" @blur="handlePasswordBlur"
                    classes="input">
            </vue-password>
        </FormItem>
        <FormItem label="Confirm Password:" prop="confirmPassword">
            <vue-password v-model="formItems.confirmPassword" @blur="handleConfirmPasswordBlur"
                    classes="input">
            </vue-password>
        </FormItem>
        <FormItem>
            <Button type="primary" @click="handleChange">Change</Button>
            <Button style="margin-left: 8px" @click="handleReset">Cancel</Button>
        </FormItem>
    </Form>
</div>
</template>

<script>
import VuePassword from 'vue-password'
import {resetMypassword} from '@/api/user'
import { LoadingBar } from 'iview'
export default {
  name: 'Password',
  components: {
      VuePassword
  },
  data() {
      const validatePassCheck = (rule, value, callback) => {
                        if (value === '') {
                            callback(new Error('Please enter your password again'));
                        } else if (value !== this.formItems.password) {
                            callback(new Error('The two input passwords do not match!'));
                        } else {
                            callback();
                        }
        };
      return {
         formItems: {
            password: '',
            confirmPassword: ''
         },
         formRules: {
            password: [{required: true, message: 'The password cannot be empty', trigger: 'blur'},
                {max: 200, min:6, trigger: 'blur'}],
            confirmPassword: [{required: true, message: 'The password cannot be empty', trigger: 'blur'},
                {max: 200, min:6, trigger: 'blur'},{validator: validatePassCheck,trigger: 'blur'}],    
         }
      }
  },
  methods: {
        handleChange () {
                this.$refs['passwordForm'].validate((valid) => {
                    if (valid) {
                        let params = {}
                        params.password = this.formItems.password
                        console.log('----start reset password')
                        LoadingBar.start()
                        resetMypassword(params).then(res => {
                            const data = res.data
                            if (res.status === 200) {
                                LoadingBar.finish()
                                this.$Message.success(data.msg)
                                this.$refs['passwordForm'].resetFields();
                            } else {
                                LoadingBar.error()
                                this.$Message.error(data.msg)
                            }
                        }).catch( err => {
                            LoadingBar.error()
                            this.$Message.error(err.response.status)
                            console.log(err.response.data)
                        })
                    }
                })
        },
        handlePasswordBlur(value) {
            this.$refs['passwordForm'].validateField('password')
        },
        handleConfirmPasswordBlur(value) {
            this.$refs['passwordForm'].validateField('confirmPassword')
        },
        handleReset () {
        this.$refs['passwordForm'].resetFields();
      }
  }
}
</script>

<style>

</style>
