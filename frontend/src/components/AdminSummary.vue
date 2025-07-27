<template>
  <div >
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">Admin Dashboard</a>

                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <router-link class="nav-link" to="/admin_home">Home</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" to="/admin_summary">Summary</router-link>
                        </li>
                    </ul>

                    <button class="btn btn-outline-light" @click="logout">Logout</button>
                </div>
            </div>
        </nav>

    <div class="row">
      <div class="col-md-6 mb-4">
        <BarChart v-if="chartData" :chart-data="chartData" :chart-options="chartOptions" />
      </div>

      <div class="col-md-6">
        <div class="card p-3">
          <h5>Total Users: {{ summary?.total_users ?? 'Loading...' }}</h5>
          <h5>Total Reservations: {{ summary?.total_reservations ?? 'Loading...' }}</h5>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import BarChart from './BarChart.vue'

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const summary = ref(null)
const chartData = ref(null)
const chartOptions = ref({
  responsive: true,
  plugins: {
    legend: {
      position: 'top'
    },
    title: {
      display: true,
      text: 'Parking Lot Summary'
    }
  }
})

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/admin/api/admin_summary', {
      withCredentials: true
    })
    summary.value = response.data

    // Prepare chart data from backend
    const labels = response.data.lots.map(lot => lot.lot_name)
    const dataPoints = response.data.lots.map(lot => lot.total_spots)

    chartData.value = {
      labels: labels,
      datasets: [{
        label: 'Total Spots per Lot',
        backgroundColor: '#42A5F5',
        data: dataPoints
      }]
    }
  } catch (error) {
    console.error('Error fetching admin summary:', error)
  }
})
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