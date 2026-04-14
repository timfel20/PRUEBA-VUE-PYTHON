<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <p class="text-gray-600">Redirigiendo al registro...</p>
  </div>
</template>

<script setup lang="ts">
await navigateTo('/registro', { replace: true })
</script>