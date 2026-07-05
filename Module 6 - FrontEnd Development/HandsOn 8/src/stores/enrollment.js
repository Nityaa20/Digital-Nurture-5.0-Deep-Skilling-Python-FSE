import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// this store keeps track of which courses the student enrolled in
// so both the header and profile page can see the same list
export const useEnrollmentStore = defineStore('enrollment', () => {

  const enrolledCourses = ref([])

  // adds up all the credits, used this in profile page
  const totalCredits = computed(() => {
    let total = 0
    for (let i = 0; i < enrolledCourses.value.length; i++) {
      total = total + enrolledCourses.value[i].credits
    }
    return total
  })

  function enroll(course) {
    // check if already enrolled so we don't add it twice
    let found = false
    for (let i = 0; i < enrolledCourses.value.length; i++) {
      if (enrolledCourses.value[i].id === course.id) {
        found = true
      }
    }
    if (!found) {
      enrolledCourses.value.push(course)
    }
    console.log('enrolled courses now:', enrolledCourses.value)
  }

  function unenroll(courseId) {
    enrolledCourses.value = enrolledCourses.value.filter(function (c) {
      return c.id !== courseId
    })
  }

  return { enrolledCourses, totalCredits, enroll, unenroll }
})
