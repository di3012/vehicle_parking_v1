<template>
  <div>

    <!-- Bootstrap Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">User Dashboard</a>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <a class="nav-link active" @click="activeTab = 'home'">Home</a>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/user_summary">Summary</router-link>
            </li>
          </ul>

          <button class="btn btn-outline-light" @click="logout">Logout</button>
        </div>
      </div>
    </nav>

    <!-- HOME TAB -->
    <div v-if="activeTab === 'home'" class="container mt-4">
      <h3>Search Parking Lots</h3>
      <SearchParking />

      <hr />

      <h4>Current Reservations</h4>
      <CurrentReservations />

      <hr />

      <h4>Past Reservation History</h4>
      <PastReservations />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import SearchParking from '@/components/SearchParking.vue'
import CurrentReservations from '@/components/CurrentReservation.vue'
import PastReservations from '@/components/PastReservation.vue'

const activeTab = ref('home')
const router = useRouter()

const logout = async () => {
  // Call backend logout to clear Flask session
  await fetch('http://localhost:5000/api/logout', {
    method: 'POST',
    credentials: 'include', // send session cookie
  })

  // Clear frontend localStorage and redirect
  localStorage.removeItem('role')
  router.push('/login')
}
</script>

<style scoped>
hr {
    margin: 2rem 0;
}

.router-link-exact-active {
  color: #fff !important;
  border-radius: 0.25rem;
}
</style>