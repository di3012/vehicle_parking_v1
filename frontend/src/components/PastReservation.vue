<template>
  <div class="container mt-4">
    <table class="table table-bordered table-striped mt-3" v-if="reservations.length">
      <thead class="table-dark">
        <tr>
            <th>Spot ID</th>
          <th>Lot Name</th>
          <th>City</th>
          <th>Address</th>
          <th>Vehicle Number</th>

          <th>From</th>
          <th>To</th>
          <th>Cost</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="res in reservations" :key="res.reservation_id">
            <td>{{ res.spot_id }}</td>
          <td>{{ res.lot_name }}</td>
          <td>{{ res.city }}</td>
          <td>{{ res.address }}</td>
          <td>{{ res.vehicle_number }}</td>
          <td>{{ res.parking_timestamp }}</td>
          <td>{{ res.leaving_timestamp }}</td>
          <td>₹{{ res.parking_cost }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else class="text-muted">No past reservations found.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const reservations = ref([])

onMounted(async () => {
  const res = await fetch('http://localhost:5000/user/api/past_reservations', {
    credentials: 'include'
  })
  if (res.ok) {
    reservations.value = await res.json()
  }
})
</script>
