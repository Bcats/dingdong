/**
 * Vue Router配置
 */
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录', noAuth: true },
  },
  {
    path: '/',
    component: () => import('@/views/Layout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '首页', icon: 'DataLine' },
      },
      {
        path: 'messages',
        name: 'Messages',
        component: () => import('@/views/Messages/Index.vue'),
        meta: { title: '消息管理', icon: 'Message' },
      },
      {
        path: 'messages/:id',
        name: 'MessageDetail',
        component: () => import('@/views/Messages/Detail.vue'),
        meta: { title: '消息详情', hidden: true },
      },
      {
        path: 'templates',
        name: 'Templates',
        component: () => import('@/views/Templates/Index.vue'),
        meta: { title: '模板管理', icon: 'Document' },
      },
      {
        path: 'email-accounts',
        name: 'EmailAccounts',
        component: () => import('@/views/EmailAccounts/Index.vue'),
        meta: { title: '邮箱管理', icon: 'Message' },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 消息通知平台`
  }

  // 如果是登录页，直接放行
  if (to.meta.noAuth) {
    next()
    return
  }

  // 检查是否已登录
  if (!userStore.token) {
    next('/login')
    return
  }

  next()
})

export default router

