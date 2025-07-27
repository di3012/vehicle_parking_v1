import { createRouter, createWebHistory } from 'vue-router'
import WelcomePage from '@/components/WelcomePage.vue'
import Login from '@/views/login.vue'
import Register from '@/views/register.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'
import UserDashboard from '@/views/UserDashboard.vue'
import AddParkinglot from '@/components/AddParkinglot.vue'
import ViewParkinglots from '@/components/ViewParkinglots.vue'
import AdminSummary from '@/components/AdminSummary.vue'
import EditParkingLot from '@/components/EditParkingLot.vue'
import SearchParking from '@/components/SearchParking.vue'
import CurrentReservation from '@/components/CurrentReservation.vue'
import PastReservation from '@/components/PastReservation.vue'
import ViewSpotStatus from '@/components/ViewSpotStatus.vue'
import ViewUsers from '@/components/ViewUsers.vue'
import UserSummary from '@/components/UserSummary.vue'

const routes = [
  { path: '/', component: WelcomePage },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/admin_home', component: AdminDashboard },
  { path: '/user_home', component: UserDashboard },
  { path: '/add_parkinglot', component: AddParkinglot },
  { path: '/view_parkinglots', component: ViewParkinglots },
  { path: '/admin_summary', component: AdminSummary },
  { path: '/edit_parkinglot/:id', component: EditParkingLot },
  { path: '/search_parkinglots', component: SearchParking },
  { path: '/current_reservations', component: CurrentReservation },
  { path: '/past_reservations', component: PastReservation },
  { path: '/lot_spots', component: ViewSpotStatus },
  { path: '/view_users', component: ViewUsers },
  { path: '/user_summary', component: UserSummary },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})
router.beforeEach((to, from, next) => {
  const role = localStorage.getItem('role')

  if (to.path.startsWith('/user') && role !== 'user') {
    next('/login')
  } else if (to.path.startsWith('/admin') && role !== 'admin') {
    next('/login')
  } else {
    next()
  }
})


export default router
