<script setup>
import Header from './components/Header.vue'
</script>

<template>
  <Header />
  <div class="main-content">
    <RouterView />
  </div>
</template>

<style>
.main-content {
  padding: 15px;
}
</style>
