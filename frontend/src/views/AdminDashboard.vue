<!-- AdminDashboard.vue -->
<template>
    <div>

        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">Admin Dashboard</a>

                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link active" @click="activeTab = 'home'">Home</a>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" to="/admin_summary">Summary</router-link>
                        </li>
                    </ul>

                    <button class="btn btn-outline-light" @click="logout">Logout</button>
                </div>
            </div>
        </nav>


        <!-- Dynamic Section Rendering -->
        <div class="container mt-4">
            <AddParkingLot v-if="activeTab === 'home'" />
            <ViewParkingLots v-if="activeTab === 'home'" />
            <ViewUsers v-if="activeTab === 'home'" />
            <ViewSpotStatus v-if="activeTab === 'home'" />
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AddParkingLot from '../components/AddParkinglot.vue'
import ViewParkingLots from '../components/ViewParkinglots.vue'
import ViewSpotStatus from '../components/ViewSpotStatus.vue'
import ViewUsers from '@/components/ViewUsers.vue'


const router = useRouter()
const activeTab = ref('home')

const logout = async () => {
    await fetch('http://localhost:5000/api/logout', {
        method: 'POST',
        credentials: 'include',
    })

    // Clear frontend localStorage and redirect
    localStorage.removeItem('role')
    router.push('/login')
}
</script>

<style scoped>
hr {
    margin: 2rem 0;
}

.router-link-exact-active {
  color: #fff !important;
  border-radius: 0.25rem;
}
</style>
