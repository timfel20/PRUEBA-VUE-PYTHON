<!-- pages/registro.vue -->
<template>
  <div class="min-h-screen bg-gray-100 py-12">
    <div class="container mx-auto">
      <RegistrationForm />
    </div>
  </div>
</template>

<script setup lang="ts">
// Importamos el formulario de registro
import { useHead } from 'nuxt/app';
import RegistrationForm from '../components/RegistrationForm.vue';

// Page metadata...titulo, descripcion, etc.
useHead({
  title: 'Registro - tualergiahoy.com',
  meta: [
    { 
      name: 'description', 
      content: 'Regístrate en tualergiahoy.com y recibe pronósticos personalizados de alergias' 
    }
  ]
})
</script>