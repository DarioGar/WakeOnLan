import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  { path: '/', redirect: '/home' },
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
    path: '/home',
    name: 'Home',
    component: () => import("@/views/Dashboard.vue")
  },
  {
    path: '/computers',
    name: 'Computers',
    component: () => import('@/views/Computers.vue')
  },
  {
    path: '/groups',
    name: 'Groups',
    component: () => import('@/views/Groups.vue')
  },
  
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
