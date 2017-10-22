import Vue from 'vue'
import Router from 'vue-router'
import Layout from '@/components/layout'
import server from '@/components/resource/server.vue'
import serverGroup from '@/components/server_group/server_group.vue'
import group from '@/components/group'
import user from '@/components/user/user'
import login from '@/components/login.vue'
import chart from '@/components/chart/chart.vue'
import { checkToken } from '../api/auth';
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
            default: server
          },
          meta: {
            title: 'Overview',
            auth: true
          }
        },
        {
          path: '/user',
          name: '用户管理',
          component: user,
          meta: {
            title: 'User',
            auth: true,
            parent: '权限管理'
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
        },
        // 资源管理
        {
          path: '/server',
          name: '服务器管理',
          component: server,
          meta: {
            title: 'Server',
            auth: true,
            parent: '资产管理'
          }
        },
        {
          path: '/server_group',
          name: '服务器分组',
          component: serverGroup,
          meta: {
            title: 'ServerGroup',
            auth: true,
            parent: '资产管理'
          }
        },
        // 图表
        {
          path: '/chart',
          name: '图表2',
          component: chart,
          meta: {
            title: 'chart',
            auth: true,
            parent: '图表'
          }
        },
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
