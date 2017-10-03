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
        padding: 10px 0;
        overflow: hidden;
    }
    .layout-ceiling-main {
        float: right;
        margin: 5px 20px 0 0;
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
              <Badge count="0"><a><Avatar v-bind:src="userInfo.src" icon="person" style="background-color: #2baee9"/></a></Badge>
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
              <Badge dot><a><Avatar icon="ios-bell" style="background-color: #2baee9"/></a></Badge>
              <div class="api" slot="content">
                <Button v-on:click="logoutClick" size="small"><Icon type="log-out"></Icon>登出</Button>
              </div>
            </Poptip>
          </div>
        </div>
        <!-- 左侧菜单 -->
        <Row type="flex">
            <Col :span="spanLeft" class="layout-menu-left">
                <Menu :active-name="select_menu.sub" theme="dark" width="auto" v-on:on-select="change_menu_name" v-on:on-open-change="change_submenu_name" accordion>
                    <div class="layout-logo-left"></div>

                    <template v-for="menu in menus" v-if="menu.path.constructor != Array">
                      <router-link :to="menu.path">
                        <MenuItem :name="menu.name">
                            <Icon :type="menu.icon" :size="iconSize"></Icon>
                            <span class="layout-text" v-text="menu.name"></span>
                        </MenuItem>
                      </router-link>
                    </template>

                    <template v-for="menu in menus" v-if="menu.path.constructor == Array">
                      <Submenu :name="menu.name">
                        <template slot="title">
                            <Icon :type="menu.icon" :size="iconSize"></Icon>
                            <span class="layout-text" v-text="menu.name"></span>
                        </template>

                        <template v-for="menu in menu.path">
                          <router-link :to="menu.path">
                            <MenuItem :name="menu.name">
                              <Icon :type="menu.icon" :size="iconSize"></Icon>
                              <span class="layout-text" v-text="menu.name"></span>
                            </MenuItem>
                          </router-link>
                        </template>
                      </Submenu>
                    </template>
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
                  </Row>
                </div>

                <div class="layout-breadcrumb">
                  <Breadcrumb>
                    <BreadcrumbItem href="#">首页</BreadcrumbItem>
                    <BreadcrumbItem href="#"><span v-text="select_menu.show"></span></BreadcrumbItem>
                    <BreadcrumbItem v-text="select_menu.sub">某应用</BreadcrumbItem>
                  </Breadcrumb>
                </div>

                <div class="layout-content">
                    <div class="layout-content-main">
                      <router-view></router-view>
                    </div>
                </div>

                <div class="layout-copy">
                    2011-2016 &copy; Super
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
                select_menu: {
                  sub: this.$route.name,
                  default: '应用中心',
                  cache: '',
                  show: this.$route.meta.parent ? this.$route.meta.parent : '应用中心',
                  single: ['Overview']
                },
                is_show: {auth: true},
                menus: [
                  {name: 'Overview', icon:'speedometer', path: '/'},
                  {name: '资产管理', icon:'ios-paper', path: [
                    {name: '服务器管理', icon:'ios-navigate', path: '/'},
                    {name: 'IDC管理', icon:'android-list', path: '/user'}
                  ]},
                  {name: '权限管理', icon:'ios-paper', path: [
                    {name: '用户管理', icon:'ios-navigate', path: '/user'},
                    {name: '项目管理', icon:'android-list', path: '/group'}
                  ]}
                ]
            }
        },
        computed: {
            iconSize () {
                return this.spanLeft === 5 ? 14 : 24;
            },
            userInfo () {
              return this.$store.getters.loginInfo ? this.$store.getters.loginInfo : {user: 'Guest'}
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
                if (this.select_menu.single.indexOf(name) == -1) {
                  this.select_menu.show = this.select_menu.cache ? this.select_menu.cache : this.select_menu.default;
                } else {
                  this.select_menu.show = this.select_menu.default;
                }
                this.select_menu.sub = name
            },
            change_submenu_name (name) {
                return this.select_menu.cache = name[0]
            },
            logoutClick () {
              this.$store.dispatch('remove_token');
              if (typeof(this.$store.state.loginInfo.token) === 'undefined') {
                this.$router.push({path: 'login'})
              }
            }
        }
    }
</script>
