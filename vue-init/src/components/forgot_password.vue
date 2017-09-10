<template>
  <div class="ui main container">
    <div class="ui centered grid">
      <div class="column">
        <h1 class="ui center aligned header">重置密码</h1>
        <form class="ui form" novalidate @submit.prevent="submit()">
          <div class="field">
            <label>我们将发送一封密码重置邮件到你的邮箱<br>点击按钮即可重置密码</label>
          </div>
          <div class="field">
            <input
              type="email"
              name="email"
              placeholder="请输入邮箱"
              v-model="params.email">
          </div>
          <div class="field">
            <button class="fluid ui primary button" type="submit">发送验证邮件</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
const toastr = global.toastr;
export default {
  data() {
    return {
      params: {
        email: '',
      },
    };
  },
  methods: {
    submit() {
      toastr.warning('功能开发中，如需帮助请联系作者。');
    },
  },
};
</script>

<style scoped>
.column {
  max-width: 400px;
}
</style>
