<style scoped>
  .wrapper {
    margin: 0 auto;
    position: relative;
    width: 400px;
    height: 300px;
    padding-top: 150px;
    padding-bottom: 200px;
  }
  .wrapper > h1{
    text-align: center;
    vertical-align: middle;
    margin-bottom: 20px;
    color: #000;
  }

  .login {
    margin: 0 auto;
    padding: 300px auto;
    width: 300px;
    /*background-color: #0b97c4;*/
    /*border: 1px solid #A0A000;*/
  }
  Button {
    width: 300px;
  }
</style>

<template>

  <div class="wrapper">
  <h1>
  Super运维平台
  </h1>

  <div class="login">

    <Form ref="formInline" :model="formInline" :rules="ruleInline">
        <FormItem prop="user">
            <Input type="text" v-model="formInline.user" placeholder="Username">
              <Icon type="ios-person-outline" slot="prepend"></Icon>
            </Input>
        </FormItem>
        <FormItem prop="password">
            <Input type="password" v-model="formInline.password" placeholder="Password">
              <Icon type="ios-locked-outline" slot="prepend"></Icon>
            </Input>
        </FormItem>
        <FormItem>
            <Button type="primary" @click="handleSubmit('formInline')">登录</Button>
        </FormItem>
             <router-link to="/forgot_password" style="float: right">忘记密码</router-link>
    </Form>
  </div>

  </div>
</template>
<script>
    export default {
        data () {
            return {
                formInline: {
                    user: '',
                    password: ''
                },
                ruleInline: {
                    user: [
                        { required: true, message: '请填写用户名', trigger: 'blur' }
                    ],
                    password: [
                        { required: true, message: '请填写密码', trigger: 'blur' },
                        { type: 'string', min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
                    ]
                }
            }
        },
        methods: {
            handleSubmit(name) {
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        this.$Message.success('提交成功!');
                        this.$router.push('/');
                    } else {
                        this.$Message.error('表单验证失败!');
                    }
                })
            }
        }
    }
</script>
