<style scoped>
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
        min-height: 650px;
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
      height: auto;
      width: auto;
      margin: 5px 0 0 15px;
    }
    .layout-hide-text .layout-text{
        display: none;
    }
    .ivu-col{
        transition: width .2s ease-in-out;
    }
    .layout-ceiling{
        background: #464c5b;
        padding: 5px 0;
        overflow: hidden;
    }
    .layout-ceiling-main {
        float: right;
        margin: 5px 15px 0 0;
        color: #2baee9;
    }
</style>
<template>
    <div class="layout" :class="{'layout-hide-text': spanLeft < 5}">
        <div class="layout-ceiling">
          <!-- 顶部左侧 -->
            <div class="layout-ceiling-left">
              <img src="../assets/logo.png" height="auto" width="30px">
            </div>
            <div class="layout-ceiling-left"><h2 style="color: #0b97c4;">Super运维平台</h2></div>
          <!-- 顶部用户 -->
          <div class="layout-ceiling-main">
            <Poptip trigger="hover" placement="bottom-end" width="220" v-bind:title="'Hello! '+userInfo.user">
              <Badge count="0"><Avatar v-bind:src="userInfo.src" icon="person" style="background-color: #2baee9"/></Badge>
              <Dropdown><Icon type="arrow-down-b"></Icon></Dropdown>
              <div class="api" slot="content">
                <Button v-on:click="logoutClick" size="small" icon="person">个人信息</Button>&nbsp;&nbsp;
                <Button v-on:click="logoutClick" size="small" icon="log-out">退出登出</Button>
              </div>
            </Poptip>
          </div>
          <!-- 顶部消息 -->
          <div class="layout-ceiling-main">
            <Poptip trigger="hover" placement="bottom-end" width="60">
              <Badge dot><Avatar icon="ios-bell" style="background-color: #2baee9"/></Badge>
              <div class="api" slot="content">
                <Button v-on:click="logoutClick" size="small"><Icon type="log-out"></Icon>登出</Button>
              </div>
            </Poptip>
          </div>
        </div>
        <!-- 左侧菜单 -->
        <Row type="flex">
            <Col :span="spanLeft" class="layout-menu-left">
                <Menu active-name="Overview" theme="dark" width="auto" v-on:on-select="change_menu_name" v-on:on-open-change="change_submenu_name" accordion>
                    <div class="layout-logo-left"></div>

                    <router-link to="/">
                    <MenuItem name="Overview">
                        <Icon type="speedometer" :size="iconSize"></Icon>
                        <span class="layout-text">Overview</span>
                    </MenuItem>
                    </router-link>

                    <Submenu name="资产管理">
                      <template slot="title">
                          <Icon type="ios-paper" :size="iconSize"></Icon>
                          <span class="layout-text">资产管理</span>
                      </template>

                      <router-link to="/">
                        <MenuItem name="服务器管理">
                          <Icon type="ios-navigate" :size="iconSize"></Icon>
                          <span class="layout-text">服务器管理</span>
                        </MenuItem>
                      </router-link>
                      <router-link to="/">
                        <MenuItem name="IDC管理">
                          <Icon type="ios-navigate" :size="iconSize"></Icon>
                          <span class="layout-text">IDC管理</span>
                        </MenuItem>
                      </router-link>
                    </Submenu>

                  <Submenu name="1">
                    <template slot="title">
                        <Icon type="ios-paper"></Icon>
                        内容管理
                    </template>
                    <MenuItem name="1-1">文章管理</MenuItem>
                  </Submenu>

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
            <!-- 右侧搜索工具栏, 主内容区-->
            <Col :span="spanRight">
                <div class="layout-header">
                  <Row type="flex" align="middle">

                    <Col span="2">
                      <Button type="text" @click="toggleClick">
                          <Icon type="navicon" size="32"></Icon>
                      </Button>
                    </Col>
                    <!-- 项目选择 -->
                    <Col span="2" offset="9">
                    <Button type="primary" shape="circle">圆角按钮</Button>
                    </Col>
                    <!-- 搜索栏 -->
                    <Col span="6" offset="3">
                      <Input v-model="searchValue" >
                      <Select v-model="selectValue" slot="prepend" style="width: 80px">
                        <Option value="ip">Ip地址</Option>
                        <Option value="idc">机房</Option>
                      </Select>
                      <Button slot="append" v-on:click="searchClick" icon="ios-search"></Button>
                      </Input>
                    </Col>

                  </Row>
                </div>

                <div class="layout-breadcrumb">
                  <Breadcrumb>
                    <BreadcrumbItem href="#">首页</BreadcrumbItem>
                    <BreadcrumbItem href="#"><span v-text="select_subname.show"></span></BreadcrumbItem>
                    <BreadcrumbItem v-text="select_name">某应用</BreadcrumbItem>
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
    export default {
        data () {
            return {
                spanLeft: 5,
                spanRight: 19,
                select_name: 'Overview',
                select_subname: {
                  default: '应用中心',
                  cache: '',
                  show: '应用中心',
                  single_memu: ['Overview', '权限管理', '3']
                },
                is_show: {auth: true},
                searchValue: '',
                selectValue: 'ip'
            }
        },
        computed: {
            iconSize () {
                return this.spanLeft === 5 ? 14 : 24;
            },
            userInfo () {
              return this.$store.getters.loginInfo
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
                if (this.select_subname.single_memu.indexOf(name) == -1) {
                  this.select_subname.show = this.select_subname.cache ? this.select_subname.cache : this.select_subname.default;
                } else {
                  this.select_subname.show = this.select_subname.default;
                }
              this.select_name = name
            },
            change_submenu_name (name) {
                return this.select_subname.cache = name[0]
            },
            logoutClick () {
              this.$store.dispatch('remove_token');
              if (typeof(this.$store.state.loginInfo.token) === 'undefined') {
                this.$router.push({path: 'login'})
              }
            },
            searchClick() {
              this.$Message.info(this.searchValue+" to "+this.selectValue)
            }
        }
    }
</script>
