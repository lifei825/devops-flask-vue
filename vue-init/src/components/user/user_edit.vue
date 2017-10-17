<template>
  <!-- 修改或添加用户 -->
  <Modal
    v-model="isEditUser"
    :title="title"
    closable
    @on-ok="saveUser"
    @on-cancel="cancelSaveUser">
    <Form ref="userItem" :model="userItem" :label-width="80">
      <FormItem label="用户名称">
        <Input v-model="userItem.username" placeholder="请输入"/>
      </FormItem>
      <FormItem label="邮箱">
        <Input v-model="userItem.email" placeholder="请输入"/>
      </FormItem>
      <FormItem label="手机">
        <Input v-model="userItem.phone" placeholder="请输入"/>
      </FormItem>
      <FormItem label="职位">
        <Input v-model="userItem.job" placeholder="请输入"/>
      </FormItem>
      <FormItem label="权限">
        <CheckboxGroup v-model="userItem.roles">
          <template v-for="(item, key) in constRoles">
            <Checkbox :label="key"><span v-text="item[1]"></span></Checkbox>
          </template>
        </CheckboxGroup>
      </FormItem>
    </Form>
  </Modal>
</template>

<script>
  export default {
    props: ['isEditUser', 'userItem', 'title'],
    data () {
      return {
      }
    },
    computed: {
      constRoles () {
        return this.$store.getters.loginInfo.roles
      }
    },
    methods: {
      saveUser() {
        console.log("edit:", this.userItem.roles)
        this.$emit('saveUser')
      },
      cancelSaveUser() {
        this.$emit('cancelSaveUser')
      }
    }
  }

</script>
