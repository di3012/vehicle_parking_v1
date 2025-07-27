<template>
  <div class="container mt-4">

    <table class="table table-bordered table-striped mt-3">
      <thead class="table-dark">
        <tr>
          <th>Spot ID</th>
          <th>Lot Name</th>
          <th>City</th>
          <th>Address</th>
          <th>Vehicle Number</th>
          <th>Start Time</th>
          <th>Cost</th>
          <th>Action</th>
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
          <td>₹{{ res.parking_cost }}</td>
          <td>
            <button class="btn btn-danger btn-sm" @click="vacateSpot(res.reservation_id)">
              Vacate
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="reservations.length === 0" class="text-muted">
      No current or upcoming reservations found.
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const reservations = ref([])

const fetchCurrentReservations = async () => {
  const res = await fetch('http://localhost:5000/user/api/current_reservations', {
    credentials: 'include'
  })
  reservations.value = await res.json()
}

const vacateSpot = async (reservation_id) => {
  if (!confirm('Are you sure you want to vacate this spot?')) return

  const res = await fetch('http://localhost:5000/user/api/vacate_spot', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ reservation_id })
  })

  const data = await res.json()
  if (res.ok) {
    alert(data.message || 'Spot vacated successfully.')
    fetchCurrentReservations()
  } else {
    alert(data.error || 'Failed to vacate spot.')
  }
}

onMounted(fetchCurrentReservations)
</script>
