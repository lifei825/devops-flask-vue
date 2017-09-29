import Vue from 'vue'
import Router from 'vue-router'
import Layout from '@/components/layout'
import service from '@/components/service.vue'
import group from '@/components/group'
import auth from '@/components/auth.vue'
import login from '@/components/login.vue'
import { checkToken } from '../api/api';
import store from '@/store'


Vue.use(Router);

const document = global.document;


const router = new Router({
  routes: [
    {
      path: '/',
      component: Layout,
      children: [
        {
          path: '/',
          name: 'Overview',
          components: {
            default: service
          },
          meta: {
            title: 'Server',
            auth: true
          }
        },
        {
          path: '/auth',
          name: '权限管理',
          component: auth,
          meta: {
            title: 'Auth',
            auth: true
          }
        },
        {
          path: '/group',
          name: '项目管理',
          component: group,
          meta: {
            title: 'Group',
            auth: true,
            parent: '权限管理'
          }
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
    }
  ]
});

router.beforeEach((to, from, next) => {
  let loginInfo = store.getters.loginInfo;
  console.log(1111111, loginInfo)

  if (to.meta.auth && loginInfo) {
    let token = loginInfo.token;

    checkToken(token).then((res) => {
      let verify = res.data.result.verify;
      if (verify) {
        next()
      } else {
        next("/login")
      }
    }).catch(res => {
      next('/login')
    });
  } else if (!loginInfo && to.meta.auth){
    console.log('2c');
    next('/login')
  } else {
    console.log('3c', to.path);
    next()

  }
});

router.afterEach((route) => {
  document.title = `${route.meta.title} - Super`;
});

export default router
