// composables/useApi.ts

import { UsuarioForm, ApiResponse } from '../app/types/usuario';
import { useRuntimeConfig, useFetch } from 'nuxt/app';

//Ka función principal que exportamos para manejar la comunicación con el backend
export const useApi = () => {
  
  //Para obtener la configiuracion y leer la URL de la API desde nuxt.config.ts
  //    Si no está configurado, use localhost como respaldo
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase || 'http://localhost:8000/api'

  // Enviar los datos del formulario de registro y de usuarios al backend
  const register = async (formData: UsuarioForm): Promise<ApiResponse> => {
    
    try {
      // useFetch, el cliente HTTP integrado de Nuxt
      const { data, error } = await useFetch<ApiResponse>(`${baseURL}/registro/`, {
        method: 'POST',                         
        body: formData,                         
        headers: {
          'Content-Type': 'application/json'   
        }
      })

      // Si hay un error en la respuesta, lo lanzamos para que el componente lo maneje
      if (error.value) {
        throw error.value
      }

      // Si no hay error, devolvemos la respuesta del backend
      return data.value as ApiResponse
      
    } catch (err: any) {
      // Si hay error de red, backend caído, etc.
      return {
        success: false,
        message: err.message || 'Error de conexión con el servidor'
      }
    }
  }

  // Para comprobar si el backend está activo antes de intentar registrar o hacer otras operaciones
  const healthCheck = async (): Promise<boolean> => {
    try {
      const { data } = await useFetch<{ status: string }>(`${baseURL}/health/`)
      return data.value?.status === 'ok'
    } catch {
      return false
    }
  }

  // Devolvemos las funciones para que sean accesibles desde los componentes que las necesiten
  return {
    register,     
    healthCheck 
  }
}