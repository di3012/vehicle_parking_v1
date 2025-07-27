<template>
  <div class="welcome-container">
    <h1>Welcome to the Parking Lot App</h1>
    <div class="button-group">
      <router-link to="/login">
        <button class="btn">Login</button>
      </router-link>
      <router-link to="/register">
        <button class="btn">Register</button>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "WelcomePage",
};
</script>

<style scoped>
.welcome-container {
  text-align: center;
  margin-top: 100px;
  font-family: Arial, sans-serif;
}

.button-group {
  margin-top: 30px;
}

.btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 12px 25px;
  margin: 0 10px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
}

.btn:hover {
  background-color: #2980b9;
}
</style>
