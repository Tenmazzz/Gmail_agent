import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/HomeView.vue'
import GmailAgent from '../views/agents/GmailAgentView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/gmail-agent', name: 'gmail-agent', component: GmailAgent },
  ],
})

export default router