<template>
  <form @submit.prevent="registerUser">
    <input v-model="name" placeholder="Name" />
    <input v-model="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Password" />
    <button type="submit">Register</button>
    <p>{{ message }}</p>

    <!-- Navigation button -->
    <p>
      Already have an account?
      <router-link to="/login">Login here</router-link>
    </p>
  </form>
</template>

<script setup>
import { ref } from 'vue'

const name = ref('')
const email = ref('')
const password = ref('')
const message = ref('')

const registerUser = async () => {
  try {
    const res = await fetch('http://localhost:5000/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: name.value,
            email: email.value,
            password: password.value
        }),
        credentials: 'include'
    })

    const data = await res.json()

    if (res.ok) {
      message.value = 'Registered successfully'
      console.log(data)
    } else {
      message.value = data.message || 'Registration failed'
    }
  } catch (err) {
    message.value = 'Network error'
    console.error(err)
  }
}
</script>
