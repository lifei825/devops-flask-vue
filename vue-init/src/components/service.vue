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
        <Col span="2" offset="9">
        <Button type="primary" shape="circle">圆角按钮</Button>
        </Col>
        <!-- 搜索栏 -->
        <Col span="9" offset="4">
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
    export default {
        data () {
            return {
                searchValue: '',
                selectValue: 'ip',
                columns1: [
                    {
                        title: '姓名',
                        key: 'name'
                    },
                    {
                        title: '年龄',
                        key: 'age'
                    },
                    {
                        title: '地址',
                        key: 'address'
                    }
                ],
                data1: [
                    {
                        name: '王小明',
                        age: 18,
                        address: '北京市朝阳区芍药居'
                    },
                    {
                        name: '张小刚',
                        age: 25,
                        address: '北京市海淀区西二旗'
                    },
                    {
                        name: '李小红',
                        age: 30,
                        address: '上海市浦东新区世纪大道'
                    },
                    {
                        name: '周小伟',
                        age: 26,
                        address: '深圳市南山区深南大道'
                    }
                ]
            }
        },
      methods: {
        searchClick() {
          this.$Message.info(this.searchValue+" to "+this.selectValue)
        }
      }
    }
</script>

