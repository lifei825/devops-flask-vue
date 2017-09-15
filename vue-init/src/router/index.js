import Vue from 'vue'
import Router from 'vue-router'
import Layout from '@/components/layout'
import service from '@/components/service.vue'
import auth from '@/components/auth.vue'
import login from '@/components/login.vue'
import forgot_password from '@/components/forgot_password.vue'
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
          name: '服务器',
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

router.beforeEach((to, from, next) => {
  let loginInfo = store.getters.loginInfo;
  console.log("loginfo bef: ", loginInfo);

  if (to.meta.auth && loginInfo) {
    let token = loginInfo.token;
    console.log("token bef: ", token);
    console.log("da yin patj:", from.path);

    checkToken(token).then((res) => {
      let verify = res.data.result.verify;
      console.log("check res:"+verify);
      if (verify) {
        next()
      } else {
        next("/login")
      }
    }).catch(res => {
      console.log(res);
      next('/login')
    });
  } else if (!loginInfo && to.path != '/login'){
    console.log("2 c", to.path);
    next('/login')
  } else {
    console.log("3 c");
    next()
    
  }
});

router.afterEach((route) => {
  document.title = `${route.meta.title} - Super`;
});

export default router
