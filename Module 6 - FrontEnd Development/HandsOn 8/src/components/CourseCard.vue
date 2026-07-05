<script setup>
// props coming in from the parent (CoursesView)
const props = defineProps({
  id: Number,
  name: String,
  code: String,
  credits: Number,
  grade: String
})

// letting the parent know when enroll is clicked
// (could have used the store directly here too, but doing it this
// way since that's what the exercise showed with props)
const emit = defineEmits(['enroll'])

function handleEnrollClick() {
  emit('enroll', { id: props.id, name: props.name, code: props.code, credits: props.credits, grade: props.grade })
}
</script>

<template>
  <div class="card">
    <RouterLink :to="'/courses/' + id">
      <h3>{{ name }}</h3>
    </RouterLink>
    <p>{{ code }}</p>
    <p>Credits: {{ credits }}</p>
    <p>Grade: {{ grade }}</p>
    <button @click="handleEnrollClick">Enroll</button>
  </div>
</template>

<style scoped>
.card {
  border: 1px solid black;
  padding: 10px;
  margin: 10px;
  border-radius: 5px;
  width: 200px;
}
</style>
