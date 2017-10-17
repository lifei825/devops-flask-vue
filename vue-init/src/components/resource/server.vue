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
        <!-- 项目选择 -->
        <Col span="2" offset="0">
        <Button type="primary" shape="circle" @click="infoServer={};isEditServer=!isEditServer;title='添加服务器'">添加服务器</Button>
        </Col>
        <!-- 搜索栏 -->
        <Col span="8" offset="14">
        <Input v-model="searchValue" >
        <Select v-model="selectGid" slot="prepend" style="width: 100px">
          <template v-for="group in groups">
            <Option :value="group.id" v-text="group.name" style="float: left"></Option>
          </template>
        </Select>
        <Button slot="append" v-on:click="searchClick" icon="ios-search"></Button>
        </Input>
        </Col>
      </Row>
        <br>
      </div>



      <Table :columns="columns1" :data="data1"></Table>
    </div>
</template>
<script>
    export default {
        data () {
            return {
                // 编辑添加服务器
                infoServer: {},
                isEditServer: false,
                title: null,
                // 搜索查询
                groups: this.groupList(),
                searchValue: '',
                selectGid: null,
                columns1: [
                    {
                        title: '主机名',
                        key: 'hostname'
                    },
                    {
                        title: '外网',
                        key: 'outside'
                    },
                    {
                        title: 'IDC',
                        key: 'idc'
                    },
                    {
                        title: '区域',
                        key: 'area'
                    },
                    {
                        title: '角色',
                        key: 'role'
                    },
                    {
                        title: '配置',
                        key: 'config',
                        width: '150px'
                    },
                    {
                        title: '状态',
                        key: 'state',
                        render: (h, params) => {
                          const row = params.row;
                          const color = row.state === 1 ? 'green' : row.state === 2 ? 'red' : 'gray';
                          const text = row.state === 1 ? '运行中' : row.state === 2 ? '未连接' : '停用';

                          return h('Tag', {props: {type: 'dot', color: color}}, text);
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
                            props: {type: 'info', size: 'small'},
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
                data1: [
                    {
                        hostname: 'web',
                        outside: '192.168.1.110',
                        idc: '阿里云',
                        area: '香港C区',
                        role: 'nginx',
                        config: 'cpu:1核 内存: 8G',
                        state: 3
                    }, {state: 1}, {state:2}
                ]
            }
        },
      methods: {
        // 搜索
        searchClick() {
          this.$Message.info(this.searchValue+" to "+this.selectValue)
        },
        // api
        groupList() {

        }
      }
    }
</script>

