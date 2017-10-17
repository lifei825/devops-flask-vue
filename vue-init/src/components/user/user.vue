<style scoped>
  .content-head {
    margin: 0 0 15px 0;
    padding: 0 0 10px 0;
    background: #fff;
    box-shadow: 0 1px 1px rgba(0,0,0,.1);
  }
</style>

<template>
  <div class="content">
    <div class="content-head">
      <Row type="flex" align="middle">
        <!-- 添加用户 -->
        <Col span="2">
        <Button v-if="selectGid!=0" type="primary" shape="circle" @click="infoUser={roles:[]};isEditUser=!isEditUser;title='添加用户'">添加用户</Button>
        </Col>
        <!-- 搜索栏 -->
        <Col span="8" offset="14">
        <Input v-model="searchValue" @on-enter="searchClick" placeholder="选择项目搜索">
        <Select v-model="selectGid" slot="prepend" style="width: 100px" @on-change="selectChange">
          <template v-if="admin">
          <Option value="0" style="float: left">全部用户</Option>
          </template>

          <template v-for="group in groups">
            <Option :value="group.id" v-text="group.name" style="float: left"></Option>
          </template>
        </Select>
        <Button slot="append" v-on:click="searchClick" icon="ios-search" ></Button>
        </Input>
        </Col>
      </Row>
    </div>

    <Table :columns="columns1" :data="data1" @on-select="select"></Table>

    <div style="margin: 10px 0 150px 0;overflow: hidden">
      <div style="float: right;">
        <Page :total="total" :current="1" @on-change="changePage" @on-page-size-change="changePageSize" show-total show-sizer></Page>
      </div>
    </div>

    <!-- 用户详情 -->
    <user_view :viewUsers="viewUser" :infoUsers="infoUser" @closeViewUsers="closeViewUser"></user_view>
    <!-- 用户修改添加 -->
    <user_edit :isEditUser="isEditUser" :title="title" :userItem="infoUser" @saveUser="saveUser" @cancelSaveUser="cancelSaveUser"></user_edit>
  </div>
</template>


<script>
  import {getUsers, getGroups, postUsers} from '../../api/auth'
  import user_view from './user_view.vue'
  import user_edit from './user_edit.vue'

  export default {
    data () {
      return {
        // 分页
        total: 0,
        page: 1,
        pageSize: 10,
        // 搜索框
        searchValue: '',
        selectGid: null,
        groups: this.groupList(),
        admin: false,
        // 添加修改用户
        title: '添加用户',
        isEditUser: false,
        // table
        viewUser: false,
        infoUser: {id: 0, username: null},
        columns1: [
          {
            type: 'selection',
            width: 60,
            align: 'center'
          },
          {
            title: 'id',
            key: 'id',
            sortable: true,
            sortType: 'desc'
          },
          {
            title: '用户',
            key: 'username'
          },
          {
            title: '邮箱',
            key: 'email'
          },
          {
            title: '手机',
            key: 'phone'
          },
          {
            title: '职位',
            key: 'job'
          },
          {
            title: '权限',
            key: 'roles',
            render: (h, params) => {
                const roles = params.row.roles;
                let text = '用户';
//                console.log(roles[0].id)
                params.row.disable = false;
                params.row.disable2 = false;

                if(this.selectGid == "0") {
                  params.row.disable = true
                  params.row.disable2 = true
                }

                for (var i = 0; i < roles.length; i++) {
                  console.log("select gid:", this.selectGid)
                  if (roles[i] == '255') {
                    text = "管理员"
                    params.row.disable = true
                    params.row.disable2 = true
                    break
                  }
                }
                return h('Poptip', {
                  props: {trigger: 'hover', title: '权限', placement: 'bottom'}
                }, [
                  h('Tag', text),
                  h('div', {slot: 'content'}, [h('ul', roles.map(item => {
                                                    return h('li', {style: {textAlign: 'left', padding: '4px'}}, this.constRoles[item][1])}
                                                ))
                                              ])
                ])
            }
          },
          {
            title: '操作',
            key: 'action',
            width: 200,
            align: 'centor',
            render: (h, params) => {
                return h('div', [
                      h('Button', {
                                    props: {type: 'info', size: 'small', if: "selectGid!=0"},
                                    style: {marginRight: '5px'},
                                    on: {click: () => {this.view(params.index)}}
                                  }, '查看'),
                      h('Button', {
                                    props: {type: 'primary', size: 'small', disabled: params.row.disable2},
                                    style: {marginRight: '5px'},
                                    on: {click: () => {this.edit(params.index)}}
                                  }, '编辑'),
                      h('Button', {
                                    props: {type: 'error', size: 'small', disabled: params.row.disable},
                                    on: {click: () => {this.remove(params.index)}}
                                  }, '删除')
                    ])
                }
            }
        ],
        data1: []
      }
    },
    computed: {
      constRoles () {
        return this.$store.getters.loginInfo.roles
      }
    },
    methods: {
      // 搜索
      searchClick() {
        this.page = 1;
        this.userList(this.searchValue);
        this.$Message.info(this.searchValue + " to " + this.selectValue)
      },
      selectChange() {
//        console.log("gid:", value)
        this.userList();
      },
      // api
      userList(keyword=null) {
        let token = this.$store.getters.loginInfo.token;
        getUsers(token, this.selectGid, this.page, this.pageSize, keyword).then((res) => {
          this.data1 = res.data.result.doc;
          this.total = res.data.result.total;
      }).
        catch(res => {
          this.$Message.error('请求失败', res.response.data.message);
      })
      },
      groupList(keyword=null) {
        let token = this.$store.getters.loginInfo.token;
        var g
        getGroups(token, 1, 100, keyword).then((res) => {
          this.groups = res.data.result.doc;
        // 如果有admin组 显示全部 否则不显示全部选项
        for(g in this.groups) {
          if(this.groups[g].id == "2"){
            this.selectGid = "0"
            this.admin = true
            break
          }
        }
        if(!this.admin) {this.selectGid = res.data.result.doc[0].id}
        // end
      }).catch(res => {
          console.log("失败", res)
          this.$Message.error('请求失败', res.response.data.message);
      })
      },
      userPost() {
        let token = this.$store.getters.loginInfo.token;
        postUsers(token, this.infoUser).then((res) => {
          console.log(res.data.result.state);
      }).
        catch(res => {
          this.$Message.error('请求失败', res.response.data.message);
      })
      },
      // table 事件
      select(selection, row) {
        console.log(selection[0].name, row.id, row.name)
      },
      view(index){
        this.viewUser = !this.viewUser
        this.infoUser = this.data1[index]
      },
      closeViewUser() {
        this.viewUser = !this.viewUser
      },
      edit(index) {
        this.infoUser = this.data1[index]
        console.log("master:", this.infoUser.roles)
        this.title = "编辑用户 ID " + this.infoUser.id
        this.isEditUser = !this.isEditUser
      },
      // 分页 事件
      changePageSize(pageSize) {
        this.pageSize = pageSize;
        this.data1 = this.userList(this.searchValue);
      },
      changePage(page) {
        this.page = page;
        this.data1 = this.userList(this.searchValue);
      },
      // 添加修改用户
      saveUser() {
        console.log("add:", this.infoUser.roles)
        this.isEditUser = !this.isEditUser
        this.infoUser['gid'] = this.selectGid
        this.userPost()
        // 保存后要更新user列表 否则roles列表里的数据会错误
        this.userList();
      },
      cancelSaveUser() {
        this.isEditUser = !this.isEditUser
        console.log(234)
      }
    },
    components: {
      user_view,
      user_edit
    }
  }
</script>
