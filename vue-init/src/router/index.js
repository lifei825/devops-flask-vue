import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Layout from '@/components/layout'
import service from '@/components/service.vue'
import auth from '@/components/auth.vue'
import login from '@/components/login.vue'
import forgot_password from '@/components/forgot_password.vue'


Vue.use(Router);

const document = global.document;


const router = new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Layout,
      children: [
        {
          path: '/',
          name: '服务器',
          component: service
        },
        {
          path: '/auth',
          name: '权限管理',
          component: auth
        }
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: login,
      meta: {
        title: '登录'
      }
    },
    {
      path: '/forgot_password',
      name: 'forgot_password',
      component: forgot_password
    }
  ]
});

router.afterEach((route) => {
  document.title = `${route.meta.title} - Super`;
});

export default router
