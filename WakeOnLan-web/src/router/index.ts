import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Navbar from '@/components/Navbar.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Home',
    component: () => import("@/views/Dashboard.vue")
  },
  {
    path: '/computers',
    name: 'Computers',
    component: () => import('../views/Computers.vue')
  },
  {
    path: '/groups',
    name: 'Groups',
    component: () => import('../views/Groups.vue')
  },
  
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
