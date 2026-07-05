<script setup>
</script>

<template>
  <div class="hero">
    <h2>Welcome to the Student Portal</h2>
    <p>Check out your courses and manage your profile.</p>
    <RouterLink to="/courses">
      <button>Explore Courses</button>
    </RouterLink>
  </div>
</template>

<style scoped>
.hero {
  text-align: center;
  padding: 40px;
}
</style>
