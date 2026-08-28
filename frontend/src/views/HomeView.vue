<template>
  <div class="p-8">
    <h1 class="text-3xl font-bold text-goku-pink mb-20">Mes Agents</h1>

    <div class="flex flex-wrap gap-10">
      <router-link
        to="/gmail-agent"
        class="bg-goku-black-secondary rounded-2xl p-6 w-64 h-32 flex flex-col items-center justify-center gap-2 cursor-pointer hover:scale-105 origin-top transition-transform duration-300"
      >
        <span class="text-2xl">✉️</span>
        <h2 class="text-lg font-semibold text-white">Agent Gmail</h2>
      </router-link>
    </div>
  </div>
</template>