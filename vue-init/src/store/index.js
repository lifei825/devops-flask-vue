import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);


export default new Vuex.Store({
  state: {
    loginInfo: {
      token: null,
      user: 'Guest',
      src: ''
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
  actions: {
    save_token ({ commit }, loginInfo) {
      commit('save_token', loginInfo)
    },
    remove_token ({commit}) {
      commit('remove_token')
    }
  }
})
