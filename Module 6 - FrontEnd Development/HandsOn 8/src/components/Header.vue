<script setup>
import { useEnrollmentStore } from '../stores/enrollment'

// getting the store here just to show the enrolled count
const store = useEnrollmentStore()
</script>

<template>
  <header class="header">
    <h1>Student Portal</h1>

    <nav>
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/courses">Courses</RouterLink>
      <RouterLink to="/profile">Profile</RouterLink>
    </nav>

    <p>Enrolled: {{ store.enrolledCourses.length }}</p>
  </header>
</template>

<style scoped>
.header {
  background-color: lightgray;
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header nav a {
  margin-left: 10px;
  text-decoration: none;
  color: black;
}
</style>
