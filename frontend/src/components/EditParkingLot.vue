<template>
  <div class="container mt-5">
    <h3>Edit Parking Lot</h3>
    <form @submit.prevent="updateLot">
        <input v-model="lot.city" placeholder="City" required />
        <input v-model="lot.prime_location_name" placeholder="Location Name" />
        <input v-model="lot.price" placeholder="Price" type="number" />
        <input v-model="lot.address" placeholder="Address" />
        <input v-model="lot.pincode" placeholder="Pincode" />
        <input v-model="lot.number_of_spots" placeholder="Number of Spots" type="number" />
        <button type="submit">Save Changes</button>
        <p class="text-success">{{ message }}</p>

    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const lot = ref({})
const message = ref('')

const fetchLot = async () => {
  const res = await fetch(`http://localhost:5000/admin/api/get_parkinglot/${route.params.id}`, { credentials: 'include' })
  lot.value = await res.json()
}

const updateLot = async () => {
  const res = await fetch(`http://localhost:5000/admin/api/update_parkinglot/${route.params.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(lot.value),
    credentials: 'include'
  })
  const data = await res.json()
  if (res.ok) {
    message.value = data.message
    setTimeout(() => router.push('/admin_home'), 1000)
  } else {
    message.value = data.error
  }
}

onMounted(fetchLot)
</script>
