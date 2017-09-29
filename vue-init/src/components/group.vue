<!--suppress ALL -->
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
        <!-- 创建项目 -->
        <Col span="2">
        <Button type="primary" shape="circle" @click="addGroup=true;title='添加项目'">添加项目</Button>
        </Col>
        <!-- 搜索栏 -->
        <Col span="8" offset="14">
        <Input v-model="searchValue" >
        <Select v-model="selectValue" slot="prepend" style="width: 100px">
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

      <!-- 修改或添加项目 -->
      <Modal
        v-model="addGroup"
        :title="title"
        closable
        @on-ok="ok"
        @on-cancel="cancel">
        <Form ref="formItem" :model="formItem" :label-width="80">
          <FormItem label="项目名称">
              <Input v-model="formItem.name" placeholder="请输入"></Input>
          </FormItem>
          <FormItem label="描述">
            <Input v-model="formItem.desc" placeholder="请输入"></Input>
          </FormItem>
        </Form>
      </Modal>
      <!-- 删除项目 确认 -->
      <Modal v-model="delGroup" width="360">
        <p slot="header" style="color:#f60;text-align:center">
            <Icon type="information-circled"></Icon>
            <span>删除确认</span>
        </p>
        <div style="text-align:center">
            <p v-text="'是否删除: '+ delName"></p>
        </div>
        <div slot="footer">
            <Button type="error" size="large" long @click="removeEnsure">删除</Button>
        </div>
      </Modal>
    </div>

</template>
<script>
    import { getGroups, postGroups, deleteGroups } from '../api/api';

    export default {
        data () {
            return {
                // 弹出框  添加项目
                formItem: {
                  id: 0,
                  name: null,
                  desc: ''
                },
                addGroup: false,
                title: '添加项目',
                // 分页
                total: 100,
                page: 1,
                pageSize: 10,
                // 搜索框
                searchValue: '',
                selectValue: 'name',
                // 删除项目
                delGroup: false,
                delIndex: 0,
                delName: null,
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
                        sortType: 'desc',
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
                                ]
                            )
                        }
                    }
                ],
                data1: this.groupList()
            }
        },
      methods: {
        // 搜索
        searchClick() {
          this.groupList(this.searchValue)
          this.$Message.info(this.searchValue+" to "+this.selectValue)
        },
        // api
        groupDel(gid) {
          let token = this.$store.getters.loginInfo.token;
          deleteGroups(token, gid).then((res) => {
            if(res.data.result) {
              this.$Message.success('删除成功')
            } else {
              this.$Message.error('删除失败: ' + res.data.result.state);
            }
        }).catch(res => {
            this.$Message.error('删除失败: ' + res.response.data.state);
        })
          this.delGroup = false
        },
        groupList(keyword=null) {
          let token = this.$store.getters.loginInfo.token;
          getGroups(token, this.page, this.pageSize, keyword).then((res) => {
              this.data1 = res.data.result.doc;
              this.total = res.data.result.total;
          }).catch(res => {
              this.$Message.error('请求失败', res.data.result.state);
          })
        },
        groupSave() {
          let token = this.$store.getters.loginInfo.token;
          postGroups(token, this.formItem).then((res) => {
            console.log(res.data.result)
          if (res.data.result) {
            this.$Message.success('删除成功')
          } else {
            this.$Message.error('请求失败: ' + res.data.state);
          }
          this.data1 = this.groupList();
        }).catch(error => {
            if(error.response)
          {
            switch (error.response.status) {
              case 403:
                this.$Message.error('请求失败: 没有权限')
                break;
              case 401:
                this.$Message.error('请求失败: token过期')
                break;
              default:
                this.$Message.error('请求失败:' + error.response.data.state)

            }
          } else {
            this.$Message.error('请求失败: 服务器无法连接')
          }
        })
          this.formItem.name = null
          this.formItem.desc = null
          this.formItem.id = 0

        },
        // table 事件
        select(selection, row) {
          console.log(selection[0].name, row.id, row.name)
        },
        edit(index) {
          this.title = '编辑项目'
          this.addGroup = true
          this.formItem.id = this.data1[index].id
          this.formItem.name = this.data1[index].name
          this.formItem.desc = this.data1[index].description
          console.log(index, this.data1[index].name, this.formItem)
        },
        remove(index) {
          this.delGroup = true
          this.delIndex = this.data1[index].id
          this.delName = this.data1[index].name
          console.log(index, this.data1[index].name)
        },
        removeEnsure() {
          this.groupDel(this.delIndex)
          this.data1 = this.groupList();
        },
        // 分页 事件
        changePageSize(pageSize) {
          this.pageSize = pageSize
          this.data1 = this.groupList();
          console.log(pageSize)
        },
        changePage(page) {
          this.page = page
          this.data1 = this.groupList();
          console.log(page)
        },
        // 弹出框
        ok () {
          this.groupSave()
        },
        cancel() {
          this.formItem.name = null
          this.formItem.desc = null
          this.formItem.id = 0
          this.$Message.info('已取消')
        }
      }
    }
</script>

