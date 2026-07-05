<script setup>
import { ref, onMounted, computed } from 'vue'
import CourseCard from '../components/CourseCard.vue'
import { useEnrollmentStore } from '../stores/enrollment'

const store = useEnrollmentStore()

const courses = ref([])
const searchTerm = ref('')
const loading = ref(true)

// runs once when the page loads
onMounted(async () => {
  try {
    const res = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5')
    const data = await res.json()

    console.log(data) // checking what we got back

    // jsonplaceholder doesn't actually give course info so making it up
    // from the post titles for now
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
    courses.value = temp
  } catch (err) {
    console.log('fetch failed', err)
  }
  loading.value = false
})

// this updates automatically whenever searchTerm changes
const filteredCourses = computed(() => {
  if (searchTerm.value === '') {
    return courses.value
  }
  return courses.value.filter(function (course) {
    return course.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  })
})

function handleEnroll(course) {
  store.enroll(course)
}
</script>

<template>
  <div class="courses">
    <h2>Courses</h2>

    <input type="text" v-model="searchTerm" placeholder="Search courses..." />

    <p v-if="loading">Loading...</p>
    <p v-if="!loading && filteredCourses.length === 0">No courses found</p>

    <div class="course-grid" v-if="!loading">
      <CourseCard
        v-for="course in filteredCourses"
        :key="course.id"
        :id="course.id"
        :name="course.name"
        :code="course.code"
        :credits="course.credits"
        :grade="course.grade"
        @enroll="handleEnroll"
      />
    </div>
  </div>
</template>

<style scoped>
.courses input {
  padding: 5px;
  margin: 10px 0;
  width: 200px;
}

.course-grid {
  display: flex;
  flex-wrap: wrap;
}
</style>
