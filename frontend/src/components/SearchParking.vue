<template>
  <div class="container mt-4">
    <input
      type="text"
      class="form-control mb-3"
      v-model="searchQuery"
      placeholder="Search by city, address, pincode, or location"
      @keyup.enter="performSearch"
    />

    <table class="table table-bordered table-striped mt-3">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>City</th>
          <th>Location</th>
          <th>Address</th>
          <th>Pincode</th>
          <th>Spots</th>
          <th>Price</th>
          <th>Reserve</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="lot in lots" :key="lot.id">
          <td>{{ lot.id }}</td>
          <td>{{ lot.city }}</td>
          <td>{{ lot.prime_location_name }}</td>
          <td>{{ lot.address }}</td>
          <td>{{ lot.pincode }}</td>
          <td>{{ lot.number_of_spots }}</td>
          <td>{{ lot.price }}</td>
          <td>
            <button variant="primary" @click="reserveNow(lot.id)">
              Reserve Now
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="lots.length === 0" class="text-muted">
      No matching parking lots found.
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const lots = ref([])
const searchQuery = ref('')

const fetchLots = async () => {
  const res = await fetch('http://localhost:5000/user/api/search_parkinglots', {
    credentials: 'include'
  })
  lots.value = await res.json()
}

const performSearch = async () => {
  const res = await fetch(
    `http://localhost:5000/user/api/search_parkinglots?q=${encodeURIComponent(searchQuery.value)}`,
    { credentials: 'include' }
  )
  lots.value = await res.json()
}

const reserveNow = async (lot_id) => {
  const vehicle_number = prompt('Enter your vehicle number:')
  if (!vehicle_number || vehicle_number.trim() === '') {
    alert('Reservation cancelled. Vehicle number is required.')
    return
  }

  try {
    const res = await fetch('http://localhost:5000/user/api/reserve_now', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ lot_id, vehicle_number })  // 🚗 send vehicle number
    })

    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Reservation failed')
    alert(`Reservation successful! Spot ID: ${data.spot_id}`)
  } catch (err) {
    alert(err.message)
  }
}

onMounted(fetchLots)
</script>
