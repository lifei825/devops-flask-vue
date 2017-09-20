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
        <Button type="primary" shape="circle" @click="addGroup">添加项目</Button>
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

      <Table :columns="columns1" :data="data1"></Table>
    </div>
</template>
<script>
    import { getGroups } from '../api/api';

    export default {
        data () {
            return {
                value: '',
                searchValue: '',
                selectValue: 'ip',
                columns1: [
                    {
                        title: 'id',
                        key: 'id'
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
        addGroup() {
          this.value = 'haha'
          this.$Modal.confirm({
              render: (h) => {
                return h('Input', {
                  props: {
                    value: this.value,
                    autofocus: true,
                    placeholder: 'Please enter your name...'
                  },
                  on: {input: (val) => {
                    this.value = val
//                    this.$Message.info(this.value)
                    }
                  }
                })
              },
            onOk: () => {
              this.$Message.info("que ding " + this.value)
            }
          })
        }
      }
    }
</script>

