<template>
  <div class="container mt-5">
    <h3>All Parking Lots</h3>
    <table class="table table-bordered table-striped mt-3">
      <thead class="table-dark">
        <tr>

          <th>ID</th>
          <th>City</th>
          <th>Location</th>
          <th>Price</th>
          <th>Address</th>
          <th>Pincode</th>
          <th>Spots</th>
          <th>Created At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="lot in lots" :key="lot.id">
          <td>{{ lot.id }}</td>
          <td>{{ lot.city }}</td>
          <td>{{ lot.prime_location_name }}</td>
          <td>{{ lot.price }}</td>
          <td>{{ lot.address }}</td>
          <td>{{ lot.pincode }}</td>
          <td>{{ lot.number_of_spots }}</td>
          <td>{{ lot.created_at }}</td>
          <td>
            <button @click="editLot(lot.id)">Edit</button>
            <button @click="deleteLot(lot.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="editingLot" class="edit-form mt-4">
      <h4>Edit Parking Lot (ID: {{ editingLot.id }})</h4>
      <form @submit.prevent="updateLot">
        <input v-model="editingLot.city" placeholder="City" />
        <input v-model="editingLot.prime_location_name" placeholder="Location Name" />
        <input v-model="editingLot.price" type="number" placeholder="Price" />
        <input v-model="editingLot.address" placeholder="Address" />
        <input v-model="editingLot.pincode" placeholder="Pincode" />
        <input v-model="editingLot.number_of_spots" type="number" placeholder="Number of Spots" />
        <button type="submit">Update</button>
        <button type="button" @click="editingLot = null">Cancel</button>
      </form>
    </div>
    <p v-if="lots.length === 0">No parking lots found.</p>
  </div>


</template>

<script setup>
import { ref, onMounted } from 'vue'

const lots = ref([])
const editingLot = ref(null) // holds lot being edited

const fetchLots = async () => {
  const res = await fetch('http://localhost:5000/admin/api/view_parkinglots', { credentials: 'include' })
  lots.value = await res.json()
}

const deleteLot = async (id) => {
  if (!confirm('Are you sure you want to delete this parking lot?')) return

  try {
    const res = await fetch(`http://localhost:5000/admin/api/delete_parkinglot/${id}`, {
      method: 'DELETE',
      credentials: 'include'
    })

    const data = await res.json()

    if (!res.ok) {
      alert(data.error || 'Failed to delete parking lot')
    } else {
      alert(data.message)
      fetchLots()
    }

  } catch (err) {
    alert('Network error during deletion')
    console.error(err)
  }
}

const editLot = async (id) => {
  const res = await fetch(`http://localhost:5000/admin/api/get_parkinglot/${id}`, { credentials: 'include' })
  editingLot.value = await res.json()
}

const updateLot = async () => {
  const res = await fetch(`http://localhost:5000/admin/api/update_parkinglot/${editingLot.value.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(editingLot.value), 
    credentials: 'include'
  })
  if (res.ok) {
  editingLot.value = null
  fetchLots()
  alert("Parking lot updated successfully!")
}
}

onMounted(fetchLots)
</script>
