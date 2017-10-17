<template>
  <!-- 修改或添加用户 -->
  <Modal
    v-model="isEditServerGroup2"
    :title="title2"
    width="650px"
    closable
    @on-ok="saveServerGroup2"
    @on-cancel="cancelServerGroup2">
    <div>
            <!-- 组信息编辑 -->
            <Form ref="serverGroupItem2" :model="serverGroupItem2" :label-width="80">
              <FormItem label="服务组名称">
                <Input v-model="serverGroupItem2.username" placeholder="请输入"/>
              </FormItem>
              <FormItem label="描述">
                <Input v-model="serverGroupItem2.description" type="textarea" placeholder="请输入"/>
              </FormItem>
              <FormItem label="服务组列表">
                <!--服务器分组穿梭框-->
                <Transfer
                  :data="data3"
                  :target-keys="targetKeys3"
                  :list-style="{width: '200px', height: '300px'}"
                  :render-format="render3"
                  :operations="['向左移动','向右移动']"
                  filterable
                  @on-change="handleChange3">
                  <!--<div :style="{float: 'right', margin: '5px'}">-->
                    <!--<Button type="ghost" size="small" @click="reloadMockData">重置</Button>-->
                    <!--<Button type="ghost" size="small" @click="reloadMockData">保存</Button>-->
                  <!--</div>-->
                </Transfer>
              </FormItem>
            </Form>
    </div>
  </Modal>
</template>

<script>
  export default {
    props: ['isEditServerGroup2', 'serverGroupItem2', 'title2'],
    data () {
      return {
        data3: [
                { "key": "1", "label": "内容1", "disabled": false },
                { "key": "2", "label": "内容2", "disabled": true },
                { "key": "3", "label": "内容3", "disabled": false }
            ],
        targetKeys3: ["1","2"]
      }
    },
    computed: {
      constRoles () {
        return this.$store.getters.loginInfo.roles
      }
    },
    methods: {
      saveServerGroup2() {
        this.$emit('saveUser')
      },
      cancelServerGroup2() {
        this.$emit('cancelSaveUser')
      },
      // 穿梭框
      render3 (item) {
            return item.key + ':' + item.label;
      },
      handleChange3 (newTargetKeys) {
            this.targetKeys = newTargetKeys;
      },
      reloadMockData () {
                this.data3 = this.getMockData();
                this.targetKeys3 = this.getTargetKeys();
      }
    }
  }
</script>
