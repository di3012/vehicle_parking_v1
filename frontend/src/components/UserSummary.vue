<!-- src/components/UserSummary.vue -->
<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">User Dashboard</a>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/user_home">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link active" to="/user_summary">Summary</router-link>
            </li>
          </ul>
          <button class="btn btn-outline-light" @click="logout">Logout</button>
        </div>
      </div>
    </nav>

    <div class="container mt-4">
      <h3>User Summary</h3>
      <div class="card p-4">
        <h5>Total Reservations: {{ summary.total_reservations }}</h5>
        <h5>Total Parking Time: {{ summary.total_parking_hours }} hours</h5>
        <h5>Total Cost: ₹{{ summary.total_cost }}</h5>
        <h5>Most Used Lot: {{ summary.most_used_lot }}</h5>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const summary = ref({
  total_reservations: 0,
  total_parking_hours: 0,
  total_cost: 0,
  most_used_lot: 'N/A'
})

const logout = async () => {
  await fetch('http://localhost:5000/api/logout', {
    method: 'POST',
    credentials: 'include'
  })
  localStorage.removeItem('user_id')
  localStorage.removeItem('role')
  router.push('/login')
}

onMounted(async () => {
  const userId = localStorage.getItem('user_id');

  if (!userId || userId === "undefined" || userId === "null") {
    console.error('User ID is missing from localStorage');
    return;
  }

  try {
    console.log("Fetching summary for user ID:", userId);
    const res = await axios.get(`http://localhost:5000/user/api/user_summary/${userId}`, {
      withCredentials: true
    });
    console.log("Summary data:", res.data);
    summary.value = res.data;
  } catch (err) {
    console.error('Failed to fetch summary:', err);
  }
});
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