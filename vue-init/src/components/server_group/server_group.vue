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
        <!-- 创建服务器分组 -->
        <Col span="2">
          <Button type="primary" shape="circle" @click="isEditServerGroup=!isEditServerGroup;title='添加服务器分组'">添加服务器分组</Button>
        </Col>
        <!-- 搜索栏 -->
        <Col span="8" offset="14">
        <Input v-model="searchValue" >
        <Select v-model="selectGid" slot="prepend" style="width: 100px">
          <Option value="name">项目</Option>
        </Select>
        <Button slot="append" v-on:click="searchClick" icon="ios-search"></Button>
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

    <!-- 服务组添加修改 -->
    <server_group_edit :isEditServerGroup2="isEditServerGroup" :title2="title" :serverGroupItem2="serverGroupItem"  @cancelServerGroup2="cancelServerGroup"></server_group_edit>
  </div>

</template>

<script>
    import server_group_edit from './server_group_edit.vue'

    export default {
      data () {
            return {
              listStyle: {
                  width: '250px',
                  height: '300px'
              },
              // 编辑添加
              serverGroupItem: {},
              isEditServerGroup: false,
              // 搜索框
              title: '添加服务组',
              searchValue: '',
              selectGid: null,
              groups: this.groupList(),
              admin: false,
              // 分页
              total: 100,
              page: 1,
              pageSize: 10,
              // table
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
                  title: '名称',
                  key: 'name'
                },
                {
                  title: '描述',
                  key: 'description'
                },
                {
                  title: '创建时间',
                  key: 'confirmed_at'
                },
                {
                  title: '操作',
                  key: 'action',
                  width: 150,
                  align: 'centor',
                  render: (h, params) => {
                  return h('div', [
                    h('Button', {
                      props: {
                        type: 'primary',
                        size: 'small'},
                      style: {
                        marginRight: '5px'},
                      on: {
                        click: () => {
                        this.edit(params.index)}}
                    }, '编辑'),
                    h('Button', {
                      props: {
                        type: 'error',
                        size: 'small'},
                      on: {
                        click: () => {
                        this.remove(params.index)}}
                    }, '删除')
                  ])
                }
              }
            ],
            data1: this.groupList()
//            data1: [{id: 1, name: "test", description: "aaa", confirmed_at: "20171015"}]
          }
      },
      methods: {
        // 搜索
        searchClick() {
          this.page = 1;
          this.userList(this.searchValue);
          this.$Message.info(this.searchValue + " to " + this.selectGid)
        },
        selectChange() {
        },
        // api
        groupList(keyword=null) {
          this.data1 = [{id: 1, name: "test", description: "aaa", confirmed_at: "20171015"}]
          return this.data1
        },
        // table 事件
        select(selection, row) {
          console.log(selection[0].name, row.id, row.name)
        },
        // 分页 事件
        changePageSize(pageSize) {
          this.pageSize = pageSize
          this.data1 = this.groupList(this.searchValue);
          console.log(pageSize)
        },
        changePage(page) {
          this.page = page
          this.data1 = this.groupList(this.searchValue);
          console.log(page)
        },
        // 添加修改用户
        cancelServerGroup() {

        }
      },
      components: {
        server_group_edit
      }
    }
</script>
