<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEnrollmentStore } from '../stores/enrollment'

const route = useRoute()
const router = useRouter()
const store = useEnrollmentStore()

const course = ref(null)
const loading = ref(true)

// probably should share this with CoursesView instead of fetching again
// but doing it this way for now since it works
onMounted(async () => {
  const res = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5')
  const data = await res.json()

  let temp = []
  for (let i = 0; i < data.length; i++) {
    temp.push({
      id: data[i].id,
      name: data[i].title.substring(0, 20),
      code: 'CS10' + i,
      credits: 3,
      grade: 'A'
    })
  }

  // route.params.id comes in as a string so converting it to compare properly
  for (let i = 0; i < temp.length; i++) {
    if (temp[i].id == route.params.id) {
      course.value = temp[i]
    }
  }

  loading.value = false
})

function handleEnroll() {
  store.enroll(course.value)
  router.push('/profile')
}
</script>

<template>
  <div class="detail">
    <p v-if="loading">Loading...</p>
    <p v-if="!loading && !course">Course not found</p>

    <div v-if="!loading && course">
      <h2>{{ course.name }}</h2>
      <p>{{ course.code }}</p>
      <p>Credits: {{ course.credits }}</p>
      <p>Grade: {{ course.grade }}</p>
      <button @click="handleEnroll">Enroll</button>
    </div>
  </div>
</template>

<style scoped>
.detail {
  max-width: 300px;
}
</style>
