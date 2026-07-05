import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CoursesView from '../views/CoursesView.vue'
import CourseDetailView from '../views/CourseDetailView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/courses', component: CoursesView },
    { path: '/courses/:id', component: CourseDetailView },
    { path: '/profile', component: ProfileView }
  ]
})

// just logging this to see it work, saw it in a tutorial
router.beforeEach((to, from) => {
  console.log('going to:', to.path)
})

export default router
