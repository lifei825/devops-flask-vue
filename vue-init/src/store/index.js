import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);


export default new Vuex.Store({
  state: {
    loginInfo: {
      token: null,
      user: 'Guest',
      src: '',
      roles: []
    },
    todos: [
      {id:1, text: '1 text', done: true},
      {id:2, text: '2 text', done: false}
    ]

  },
  getters: {
    doneTodos: state => {
      return state.todos.filter(todo => todo.id === 1)
    },
    loginInfo: state => {
      state.loginInfo = JSON.parse(localStorage.getItem('loginInfo'));
      return state.loginInfo
    }
  },
  // Mutation同步更改 Vuex 的 store 中的状态, 组件中使用 this.$store.commit('xxx') 提交 mutation
  mutations: {
    save_token (state, loginInfo) {
      state.loginInfo = loginInfo;
      localStorage.setItem('loginInfo', JSON.stringify(loginInfo));
    },
    remove_token (state) {
      state.loginInfo = {};
      localStorage.removeItem('loginInfo')
    }
  },
  // Action 可以包含任意异步操作, 组件中使用 this.$store.dispatch('xxx') 分发 action
  actions: {
    save_token ({ commit }, loginInfo) {
      commit('save_token', loginInfo)
    },
    remove_token ({commit}) {
      commit('remove_token')
    }
  }
})
