<template>
  <div class="mt-5">
    <h3 class="mb-4">All Users</h3>

    <table v-if="users.length" class="table table-bordered table-striped mt-3">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Phone</th>
          <th>Reservations</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.phone }}</td>
          <td>{{ user.reservation_count }}</td>
          <td>
            <button class="btn btn-sm btn-danger" @click="confirmDelete(user)">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="!users.length">No users found.</p>

    <!-- Delete Confirmation Modal -->
    <div
      class="modal fade"
      id="deleteModal"
      tabindex="-1"
      aria-labelledby="deleteModalLabel"
      aria-hidden="true"
      ref="deleteModalRef"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title" id="deleteModalLabel">Confirm Delete</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" />
          </div>
          <div class="modal-body">
            Are you sure you want to delete <strong>{{ userToDelete?.name }}</strong> (ID: {{ userToDelete?.id }})?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="deleteUser">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const users = ref([])
const userToDelete = ref(null)
let modalInstance = null

const deleteModalRef = ref(null)

const fetchUsers = async () => {
  const res = await fetch('http://localhost:5000/admin/api/users', {
    credentials: 'include'
  })
  users.value = await res.json()
}

const confirmDelete = (user) => {
  userToDelete.value = user
  if (!modalInstance) {
    const modalEl = deleteModalRef.value
    modalInstance = new bootstrap.Modal(modalEl)
  }
  modalInstance.show()
}

const deleteUser = async () => {
  const userId = userToDelete.value.id

  const res = await fetch(`http://localhost:5000/admin/api/delete_user/${userId}`, {
    method: 'DELETE',
    credentials: 'include'
  })

  const data = await res.json()
  if (res.ok) {
    users.value = users.value.filter(u => u.id !== userId)
    modalInstance.hide()
    alert('User deleted successfully')
  } else {
    alert(`Error: ${data.error || 'Failed to delete user'}`)
  }
}

onMounted(fetchUsers)
</script>
