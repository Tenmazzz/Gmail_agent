<script setup>
import AppHeader from './components/AppHeader.vue'
</script>

<template>
  <div class="min-h-screen w-full bg-goku-black text-white">
    <AppHeader />
    <router-view />
  </div>
</template>