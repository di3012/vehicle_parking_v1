<template>
    <form @submit.prevent="loginUser">
        <input v-model="email" placeholder="Email" />
        <input v-model="password" type="password" placeholder="Password" />
        <button type="submit">Login</button>
        <p>{{ message }}</p>

        <!-- Navigation button -->
        <p>
            Don't have an account?
            <router-link to="/register">Register here</router-link>
        </p>
    </form>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')
const message = ref('')

const loginUser = async () => {
    try {
        const res = await fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email.value, password: password.value }),
            credentials: 'include'
        })

        const data = await res.json()
        if (res.ok) {
            message.value = 'Login successful'  
            localStorage.setItem('role', data.role)
            localStorage.setItem('user_id', data.user_id)
            // Redirect based on role
            if (data.role === 'admin') {
                router.push('/admin_home')
            } else {
                router.push('/user_home')
            }

        } else {
            message.value = data.message
        }
    } catch (err) {
        message.value = 'Network error'
    }
}
</script>
