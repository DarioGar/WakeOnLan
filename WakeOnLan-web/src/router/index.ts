import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  { path: '/', redirect: '/login' },
  {
    path: '/user',
    name: 'Users',
    component: () => import('@/views/Users.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/computers',
    name: 'Computers',
    component: () => import('@/views/Computers.vue')
  },
  {
    path: '/pc',
    name: 'My Computers',
    component: () => import('@/views/MyComputers.vue')
  },
  {
    path: '/groups',
    name: 'Groups',
    component: () => import('@/views/Groups.vue')
  },
  {
    path: '/rooms',
    name: 'Rooms',
    component: () => import('@/views/Rooms.vue')
  },
  
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
