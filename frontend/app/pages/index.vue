<!-- app/pages/index.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center">
    <p>Redirigiendo al registro...</p>
  </div>
</template>

<script setup lang="ts">
// Redirect to /registro immediately
await navigateTo('/registro', { replace: true })
</script>