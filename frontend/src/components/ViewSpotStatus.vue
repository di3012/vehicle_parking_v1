<template>
  <div class="container mt-5">
    <h3>Select Parking Lot</h3>
    <select v-model="selectedLotId" class="form-select mb-3" @change="fetchSpots">
      <option disabled value="">-- Select a Lot --</option>
      <option v-for="lot in lots" :key="lot.id" :value="lot.id">
        {{ lot.prime_location_name }} (ID: {{ lot.id }})
      </option>
    </select>

    <table v-if="spots.length" class="table table-bordered table-striped mt-3">
      <thead class="table-dark">
        <tr>
          <th>Spot ID</th>
          <th>Status</th>
          <th>Reserved By</th>
          <th>Vehicle Number</th>
          <th>From</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="spot in spots" :key="spot.spot_id">
          <td>{{ spot.spot_id }}</td>
          <td>{{ spot.status === 'A' ? 'Available' : 'Occupied' }}</td>
          <td v-if="spot.reserved_by">{{ spot.reserved_by.name }} ({{ spot.reserved_by.email }})</td>
          <td v-else colspan="3">-</td>
          <td v-if="spot.reserved_by">{{ spot.reserved_by.vehicle_number }}</td>
          <td v-if="spot.reserved_by">{{ formatDate(spot.reserved_by.from) }}</td>
        </tr>
      </tbody>
    </table>

    <p v-if="selectedLotId && !spots.length">No spots found.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const lots = ref([])
const selectedLotId = ref('')
const spots = ref([])

const fetchLots = async () => {
  const res = await fetch('http://localhost:5000/admin/api/view_parkinglots', {
    credentials: 'include'
  })
  lots.value = await res.json()
}

const fetchSpots = async () => {
  if (!selectedLotId.value) return

  const res = await fetch(`http://localhost:5000/admin/api/lot_spots/${selectedLotId.value}`, {
    credentials: 'include'
  })

  spots.value = await res.json()
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString()
}

onMounted(fetchLots)
</script>
