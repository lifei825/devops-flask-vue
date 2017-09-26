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
        <Button type="primary" shape="circle" @click="addGroup = true">添加项目</Button>
        </Col>
        <!-- 搜索栏 -->
        <Col span="8" offset="14">
        <Input v-model="searchValue" >
        <Select v-model="selectValue" slot="prepend" style="width: 100px">
          <Option value="ip">Ip地址</Option>
          <Option value="idc">机房</Option>
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

      <Modal
        v-model="addGroup"
        title="添加项目"
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
    </div>

</template>
<script>
    import { getGroups, postGroups } from '../api/api';

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
                // 分页
                total: 100,
                // 搜索框
                searchValue: '',
                selectValue: 'ip',
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
                        sortable: true
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
        searchClick() {
          this.$Message.info(this.searchValue+" to "+this.selectValue)
        },
        groupList() {
          let token = this.$store.getters.loginInfo.token;
          getGroups(token).then((res) => {
              this.data1 = res.data.result;
          }).catch(res => {
              this.$Message.error('请求失败', res.data.result.state);
          })
        },
        // table 事件
        select(selection, row) {
          console.log(selection[0].name, row.id, row.name)
        },
        edit(index) {
          console.log(index, this.data1[index].name)
        },
        remove(index) {
          console.log(index, this.data1[index].name)
        },
        // 分页 事件
        changePageSize(pageSize) {
          console.log(pageSize)
        },
        changePage(page) {
          console.log(page)
        },
        // 弹出框
        ok () {
          console.log(this.formItem.name)
          let token = this.$store.getters.loginInfo.token;
          postGroups(token, this.formItem).then((res) => {
            console.log(res.data.result)
            if (res.data.result) {
              this.$Message.success('创建成功')
            } else {
              this.$Message.error('请求失败', res.data.state);
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
        },
        cancel() {
          this.formItem.name = null
          this.formItem.desc = null
          this.$Message.info('已取消')
        },
        groupAdd() {
        }
      }
    }
</script>

