<template>
  <!-- 修改或添加项目 -->
  <Modal v-model="viewUsers" title="查看用户" @on-cancel="closeUserInfo">
    <p slot="header" style="text-align:left">
      <Icon type="information-circled" color="#2baee9"></Icon>
      <span>用户详情</span>
    </p>
    <div >
      <Row>
        <Col span="5" offset="1">用户ID:</Col>
        <p v-text="infoUsers.id"></p>
      </Row>
      <br>
      <Row>
        <Col span="5" offset="1">用户名:</Col>
        <p v-text="infoUsers.username"></p>
      </Row>
      <br>
      <Row>
        <Col span="5" offset="1">邮箱:</Col>
        <span v-text="infoUsers.email"></span>
      </Row>
      <br>
      <Row>
        <Col span="5" offset="1">手机:</Col>
        <span v-text="infoUsers.phone"></span>
      </Row>
      <br>
      <Row>
        <Col span="5" offset="1">职位:</Col>
        <span v-text="infoUsers.job"></span>
      </Row>
      <br>
      <Row>
        <Col span="5" offset="1">状态:</Col>
        <span v-text="infoUsers.active == true ? '激活' : '禁用' "></span>
      </Row>
      <br>
      <Row>
        <Col span="5" offset="1">角色:</Col>
        <template v-for="role, index in infoUsers.roles">
            <span v-text="(index+1)+'.'+constRoles[role][1]+';'"></span>&nbsp;
        </template>
      </Row>
      <br>
      <Row>
        <Col span="5" offset="1">最后登录时间:</Col>
        <span v-text="infoUsers.last_login_at"></span>
      </Row>
      <br>
      <Row>
        <Col span="5" offset="1">最后登录IP:</Col>
        <span v-text="infoUsers.last_login_ip"></span>
      </Row>
      <br>
      <Row>
        <Col span="5" offset="1">上次登录时间:</Col>
        <span v-text="infoUsers.current_login_at"></span>
      </Row>
      <br>
      <Row>
        <Col span="5" offset="1">上次登录IP:</Col>
        <span v-text="infoUsers.current_login_ip"></span>
      </Row>
      <br>

    </div>
    <div slot="footer">
      <Button type="ghost" size="large" long @click="closeUserInfo">关闭</Button>
    </div>
  </Modal>

</template>

<script>
  export default {
    props: ['viewUsers', 'infoUsers'],
    computed: {
      constRoles () {
        return this.$store.getters.loginInfo.roles
      }
    },
    methods: {
      closeUserInfo() {
        console.log("zujian el:", this.$el);
        this.$emit('closeViewUsers')
      }
    }
  }

</script>
