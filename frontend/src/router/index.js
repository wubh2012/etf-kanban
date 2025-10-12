import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: Home
  },
  {
    path: '/about',
    name: 'AboutPage',
    // 路由级代码分割，生成单独的chunk
    // 访问路由时才会加载对应组件
    component: () => import('../views/About.vue')
  },
  {
    path: '/data-maintenance',
    name: 'DataMaintenance',
    component: () => import('../views/DataMaintenance.vue')
  }
]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

export default router