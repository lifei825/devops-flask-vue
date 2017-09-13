<style scoped>

    html, body {
        height: 100%;
        margin: 0px;
        padding: 0px;
    }

    .layout{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
        position: relative;
        border-radius: 4px;
        overflow: hidden;
    }
    .layout-breadcrumb{
        padding: 10px 15px 0;
    }
    .layout-content{
        min-height: 550px;
        margin: 15px;
        overflow: hidden;
        background: #fff;
        border-radius: 4px;
    }
    .layout-content-main{
        padding: 10px;
    }
    .layout-copy{
        text-align: center;
        padding: 10px 0 20px;
        color: #9ea7b4;
    }
    .layout-menu-left{
        background: #464c5b;
    }
    .layout-header{
        height: 60px;
        background: #fff;
        box-shadow: 0 1px 1px rgba(0,0,0,.1);
    }
    .layout-logo-left{
        width: 90%;
        height: 30px;
        background: #5b6270;
        border-radius: 3px;
        margin: 15px auto;
    }
    .layout-ceiling-left{
      float: left;
      height: 20px;
      width: 20px;
      margin-left: 15px;
    }
    .layout-ceiling-main a{
        color: #9ba7b5;
    }
    .layout-hide-text .layout-text{
        display: none;
    }
    .ivu-col{
        transition: width .2s ease-in-out;
    }
    .layout-ceiling{
        background: #464c5b;
        padding: 10px 0;
        overflow: hidden;
    }
    .layout-ceiling-main{
        float: right;
        margin-right: 15px;
    }
    .layout-ceiling-main a{
        color: #9ba7b5;
    }

</style>
<template>
    <div class="layout" :class="{'layout-hide-text': spanLeft < 5}">
        <div class="layout-ceiling">
            <div class="layout-ceiling-left"><img src="../assets/logo.png" height="20px" width="20px"></div>
            <div class="layout-ceiling-main">
                <a href="#/login">注册登录</a> |
                <a href="#">帮助中心</a> |
                <a href="#">安全中心</a> |
                <a href="#">服务大厅</a> |
                <a href="#">退出登录</a> |
            </div>
        </div>
        <Row type="flex">
            <Col :span="spanLeft" class="layout-menu-left">
                <Menu active-name="服务器管理" theme="dark" width="auto" v-on:on-select="change_menu_name">
                    <div class="layout-logo-left"></div>

                    <router-link to="/">
                    <MenuItem name="服务器管理">
                        <Icon type="ios-navigate" :size="iconSize"></Icon>
                        <span class="layout-text">服务器管理</span>
                    </MenuItem>
                    </router-link>

                    <router-link to="/auth">
                    <MenuItem name="权限管理"  v-show="is_show.auth">
                        <Icon type="ios-keypad" :size="iconSize"></Icon>
                        <span class="layout-text">权限管理</span>
                    </MenuItem>
                    </router-link>

                    <MenuItem name="3">
                        <Icon type="ios-analytics" :size="iconSize"></Icon>
                        <span class="layout-text">选项 3</span>
                    </MenuItem>
                </Menu>
            </Col>
            <Col :span="spanRight">
                <div class="layout-header">
                    <Button type="text" @click="toggleClick">
                        <Icon type="navicon" size="32"></Icon>
                    </Button>
                </div>
                <div class="layout-breadcrumb">
                    <Breadcrumb>
                        <BreadcrumbItem href="/">首页</BreadcrumbItem>
                        <BreadcrumbItem href="#">应用中心</BreadcrumbItem>
                        <BreadcrumbItem v-text="select_name"></BreadcrumbItem>
                    </Breadcrumb>
                </div>
                <div class="layout-content">
                    <div class="layout-content-main">内容区域
                      <router-view></router-view>
                    </div>
                </div>
                <div class="layout-copy">
                    2011-2016 &copy; TalkingData
                </div>
            </Col>
        </Row>
    </div>
</template>
<script>
    import store from '../store'

    export default {
        data () {
            return {
                spanLeft: 5,
                spanRight: 19,
                select_name: '服务器管理',
                is_show: {auth: true}
            }
        },
        computed: {
            iconSize () {
                return this.spanLeft === 5 ? 14 : 24;
            }
        },
        methods: {
            toggleClick () {
                if (this.spanLeft === 5) {
                    this.spanLeft = 2;
                    this.spanRight = 22;
                } else {
                    this.spanLeft = 5;
                    this.spanRight = 19;
                }
            },
            change_menu_name (name) {
                console.log('layout save:', this.$store.getters.loginInfo.user);
                return this.select_name = name
            }
        }
    }
</script>
