<style scoped>
    .layout{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
        position: relative;
        border-radius: 4px;
        overflow: auto;
    }
    .layout-copy{
        text-align: center;
        /*padding: 10px 0 20px;*/
        color: #9ea7b4;
    }
    .layout-ceiling{
        background: #464c5b;
        padding: 10px 0;
        overflow: hidden;
    }
    .layout-ceiling-left{
      float: left;
      color: #00A000;
      height: 20px;
      width: 20px;
      margin-left: 15px;
    }
    .layout-ceiling-main{
        float: right;
        margin-right: 15px;
    }
    .layout-ceiling-main a{
        color: #9ba7b5;
    }

    .wrapper {
    margin: 0 auto;
    /*position: relative;*/
    width: 300px;
    height: 700px;
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
    /*padding: 300px auto;*/
    width: auto;
    /*background-color: #0b97c4;*/
    /*border: 1px solid #A0A000;*/
  }
  Button {
    width: 300px;
  }
</style>
<template>
    <div class="layout">
        <div class="layout-ceiling">
            <div class="layout-ceiling-left"><img src="../assets/logo.png" height="20px" width="20px"></div>
            <div class="layout-ceiling-main">
                <a href="#">注册登录</a> |
                <a href="#">帮助中心</a> |
                <a href="#">安全中心</a> |
                <a href="#">服务大厅</a>
            </div>
        </div>
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
        <div class="layout-copy">
            2017-2018 &copy; Super
        </div>
    </div>
</template>
<script>
    import { getUserInfo, userLogin } from '../api/api';

    export default {
      data () {
        return {
          formInline: {
            user: 'lifei',
            password: '123'
          },
          ruleInline: {
            user: [
              { required: true, message: '请填写用户名', trigger: 'blur' }
            ],
            password: [
              { required: true, message: '请填写密码', trigger: 'blur' },
              { type: 'string', min: 2, message: '密码长度不能小于6位', trigger: 'blur' }
            ]
          }
        }
      },
      methods: {
        handleSubmit(name) {
          this.$Loading.start();
          this.$refs[name].validate((valid) => {
            console.log(valid);
            if (valid) {
              userLogin(this.formInline.user, this.formInline.password).then((res) => {
                this.$store.dispatch('save_token', {
                  'user': res.data.result.username,
                  'token': res.data.result.token,
                  'src': res.data.result.src
                });
                this.$Message.success('提交成功!');
                this.$router.push('/');
                this.$Loading.finish()
              }).catch(res => {
                console.log('error:', res);
                this.$Message.error('用户名或密码验证失败!');
                this.$Loading.error()
              })
            } else {
              this.$Message.error('表单验证失败!');
            }
          })
        }
      }

    }
</script>
