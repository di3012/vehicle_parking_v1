<template>
  <div class="container mt-5">
    <h3>Add New Parking Lot</h3>
    <form @submit.prevent="addLot" class="row g-3">
      <input class="form-control" v-model="lot.city" placeholder="City" required />
      <input class="form-control" v-model="lot.prime_location_name" placeholder="Location Name" required />
      <input class="form-control" v-model="lot.price" placeholder="Price" type="number" required />
      <input class="form-control" v-model="lot.address" placeholder="Address" required />
      <input class="form-control" v-model="lot.pincode" placeholder="Pincode" required />
      <input class="form-control" v-model="lot.number_of_spots" placeholder="Number of Spots" type="number" required />
      <button class="btn btn-primary" type="submit" style="background-color: black;">Add Lot</button>
      <p class="text-success">{{ message }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const lot = ref({
  city: '',
  prime_location_name: '',
  price: '',
  address: '',
  pincode: '',
  number_of_spots: ''
})
console.log('Submitting lot:', lot.value)


const message = ref('')
const addLot = async () => {
  try {
    const res = await fetch('http://localhost:5000/admin/api/add_parkinglot', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(lot.value)
    })

    const data = await res.json()

    if (res.ok) {
      message.value = data.message || 'Lot added successfully!'
    } else {
      message.value = data.error || 'Failed to add parking lot.'
    }
  } catch (err) {
    message.value = 'Network error while adding lot.'
    console.error(err)
  }
}
</script>
