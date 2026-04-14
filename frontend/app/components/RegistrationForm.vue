<!-- components/RegistrationForm.vue -->
<template>
  <form @submit.prevent="handleSubmit" class="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
    
    <h2 class="text-2xl font-bold mb-6 text-gray-800">
      Registro - tualergiahoy.com
    </h2>
    
    <!-- Nombre -->
    <div class="mb-4">
      <label class="block text-gray-700 text-sm font-bold mb-2" for="nombre">
        Nombre *
      </label>
      <input
        id="nombre"
        v-model="form.nombre"
        type="text"
        required
        class="w-full px-3 py-2 border border-gray-300 rounded-md"
        :class="{ 'border-red-500': errors.nombre }"
        placeholder="Ej: María"
      />
      <p v-if="errors.nombre" class="text-red-500 text-xs mt-1">
        {{ errors.nombre }}
      </p>
    </div>

    <!-- Apellidos -->
    <div class="mb-4">
      <label class="block text-gray-700 text-sm font-bold mb-2" for="apellidos">
        Apellidos *
      </label>
      <input
        id="apellidos"
        v-model="form.apellidos"
        type="text"
        required
        class="w-full px-3 py-2 border border-gray-300 rounded-md"
        :class="{ 'border-red-500': errors.apellidos }"
        placeholder="Ej: García López"
      />
      <p v-if="errors.apellidos" class="text-red-500 text-xs mt-1">
        {{ errors.apellidos }}
      </p>
    </div>

    <!-- Fecha de nacimiento -->
    <div class="mb-4">
      <label class="block text-gray-700 text-sm font-bold mb-2" for="fecha_nacimiento">
        Fecha de nacimiento *
      </label>
      <input
        id="fecha_nacimiento"
        v-model="form.fecha_nacimiento"
        type="date"
        required
        class="w-full px-3 py-2 border border-gray-300 rounded-md"
        :class="{ 'border-red-500': errors.fecha_nacimiento }"
      />
      <p v-if="errors.fecha_nacimiento" class="text-red-500 text-xs mt-1">
        {{ errors.fecha_nacimiento }}
      </p>
    </div>

    <!-- Ciudad -->
    <div class="mb-4">
      <label class="block text-gray-700 text-sm font-bold mb-2" for="ciudad">
        Ciudad *
      </label>
      <input
        id="ciudad"
        v-model="form.ciudad"
        type="text"
        required
        class="w-full px-3 py-2 border border-gray-300 rounded-md"
        :class="{ 'border-red-500': errors.ciudad }"
        placeholder="Ej: Madrid"
      />
      <p v-if="errors.ciudad" class="text-red-500 text-xs mt-1">
        {{ errors.ciudad }}
      </p>
    </div>

    <!-- Alergias (checkboxes) -->
    <div class="mb-4">
      <label class="block text-gray-700 text-sm font-bold mb-2">
        Alergias conocidas
      </label>
      <div class="grid grid-cols-2 gap-2">
        <label v-for="alergia in alergiasOptions" :key="alergia" class="flex items-center">
          <input
            type="checkbox"
            :value="alergia"
            v-model="form.alergias"
            class="mr-2"
          />
          {{ alergia }}
        </label>
      </div>
      <p v-if="errors.alergias" class="text-red-500 text-xs mt-1">
        {{ errors.alergias }}
      </p>
    </div>

    <!-- Email -->
    <div class="mb-4">
      <label class="block text-gray-700 text-sm font-bold mb-2" for="email">
        Correo electrónico *
      </label>
      <input
        id="email"
        v-model="form.email"
        type="email"
        required
        class="w-full px-3 py-2 border border-gray-300 rounded-md"
        :class="{ 'border-red-500': errors.email }"
        placeholder="ejemplo@correo.com"
      />
      <p v-if="errors.email" class="text-red-500 text-xs mt-1">
        {{ errors.email }}
      </p>
    </div>

    <!-- Contraseña -->
    <div class="mb-6">
      <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
        Contraseña *
      </label>
      <input
        id="password"
        v-model="form.password"
        type="password"
        required
        minlength="6"
        class="w-full px-3 py-2 border border-gray-300 rounded-md"
        :class="{ 'border-red-500': errors.password }"
        placeholder="Mínimo 6 caracteres"
      />
      <p v-if="errors.password" class="text-red-500 text-xs mt-1">
        {{ errors.password }}
      </p>
    </div>

    <!-- Botón Enviar -->
    <button
      type="submit"
      :disabled="loading"
      class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md disabled:opacity-50"
    >
      {{ loading ? 'Registrando...' : 'Registrarse' }}
    </button>

    <!-- Mensaje de éxito -->
    <div v-if="success" class="mt-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded-md">
      <p class="font-bold">¡Registro exitoso!</p>
      <p>{{ successMessage }}</p>
      <p v-if="sheetsSynced" class="text-sm mt-2"> Sincronizado con Google Sheets</p>
    </div>

    <!-- Mensaje de error -->
    <div v-if="apiError" class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-md">
      <p class="font-bold">Error</p>
      <p>{{ apiError }}</p>
    </div>

  </form>
</template>



<script setup lang="ts">
import { reactive, ref } from 'vue'
import type { UsuarioForm, ApiError } from '../types/usuario'
import { useApi } from '../composables/useApi'

// Los datos del formulario (reactivo -se actualiza automáticamente)
const form = reactive<UsuarioForm>({
  nombre: '',
  apellidos: '',
  fecha_nacimiento: '',
  ciudad: '',
  alergias: [],
  email: '',
  password: ''
})

// Variables de estado para manejar la UI
const loading = ref(false)           // Se estando procesando el registro?
const success = ref(false)           // Hay exito en el registro?
const successMessage = ref('')       // Mensaje de éxito
const sheetsSynced = ref(false)      // Funcionó la sincronización con Google Sheets?
const apiError = ref('')             // Mensaje de error general
const errors = ref<Record<string, string>>({})  // Mensaje de error para cada campo

// Lista de opciones de alergias para los checkboxes
const alergiasOptions = [
  'polen', 'gramíneas', 'olivo', 'ácaros', 'moho',
  'epitelios de animales', 'alimentos', 'látex',
  'medicamentos', 'picaduras de insectos'
]

// Importamos la función de useApi para llamar a la API
const { register } = useApi()

// Funcion connectada al submit del formulario"
const handleSubmit = async () => {
  // Reset all states
  loading.value = true
  success.value = false
  apiError.value = ''
  errors.value = {}
  
  try {
    // Enviar los datos del formulario al backend 
    const response = await register(form)
    
    if (response.success) {
      success.value = true
      successMessage.value = response.message
      sheetsSynced.value = response.sheets_synced || false
    } else {
      // Si hay error de valiacion desde el backend, lo mostramos
      apiError.value = response.message
      
      const apiErrors = (response as ApiError).errors
      if (apiErrors) {
        // Adjunntar errores específicos de cada campo para mostrar debajo de cada input
        Object.keys(apiErrors).forEach(field => {
          if (apiErrors[field] && apiErrors[field].length > 0) {
            const errorMsg = apiErrors[field][0]
            if (errorMsg) {
              errors.value[field] = errorMsg
            }
          }
        })
      }
    }
  } catch (err: any) {
    // Erro de red, backend caído, etc.
    apiError.value = 'Error de conexión. Verifica que el servidor esté funcionando.'
  } finally {
    loading.value = false
  }
}
</script>