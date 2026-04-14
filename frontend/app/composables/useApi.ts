// composables/useApi.ts
import type { UsuarioForm, ApiResponse } from '~/types/usuario'

export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase || 'http://localhost:8000/api'

  const register = async (formData: UsuarioForm): Promise<ApiResponse> => {
    try {
      // Usamos $fetch para hacer la solicitud POST al endpoint de registro
      const data = await $fetch<ApiResponse>(`${baseURL}/registro/`, {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'application/json'
        }
      })

      return data
    } catch (err: any) {
      return {
        success: false,
        message: err.message || 'Error de conexión con el servidor'
      }
    }
  }

  const healthCheck = async (): Promise<boolean> => {
    try {
      const data = await $fetch<{ status: string }>(`${baseURL}/health/`)
      return data?.status === 'ok'
    } catch {
      return false
    }
  }

  return {
    register,
    healthCheck
  }
}