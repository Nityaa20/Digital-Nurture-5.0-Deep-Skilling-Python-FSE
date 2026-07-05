<script setup>
import { ref } from 'vue'
import { useEnrollmentStore } from '../stores/enrollment'

const store = useEnrollmentStore()

// just using separate refs for each field, seemed easier than
// one big object for now
const name = ref('')
const email = ref('')
const semester = ref('')

function handleSubmit() {
  console.log('saving profile', name.value, email.value, semester.value)
  alert('Profile saved (check console)')
}

function removeCourse(id) {
  store.unenroll(id)
}
</script>

<template>
  <div class="profile">
    <h2>Student Profile</h2>

    <form @submit.prevent="handleSubmit">
      <label>Name</label>
      <input type="text" v-model="name" />

      <label>Email</label>
      <input type="email" v-model="email" />

      <label>Semester</label>
      <input type="number" v-model="semester" />

      <button type="submit">Save</button>
    </form>

    <h3>Enrolled Courses ({{ store.enrolledCourses.length }})</h3>
    <p>Total Credits: {{ store.totalCredits }}</p>

    <p v-if="store.enrolledCourses.length === 0">No courses enrolled yet.</p>

    <ul>
      <li v-for="course in store.enrolledCourses" :key="course.id">
        {{ course.name }} ({{ course.code }}) - {{ course.credits }} credits
        <button @click="removeCourse(course.id)">Remove</button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.profile {
  max-width: 300px;
}

.profile input {
  display: block;
  margin-bottom: 8px;
  padding: 5px;
  width: 100%;
}
</style>
