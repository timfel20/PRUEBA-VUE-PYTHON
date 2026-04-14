// types/usuario.ts

// Lo que enviamos AL backend para registrar un usuario
export interface UsuarioForm {
  nombre: string
  apellidos: string
  fecha_nacimiento: string
  ciudad: string
  alergias: string[]
  email: string
  password: string
}

// Lo que recibimos DEL backend después de registrar un usuario 
export interface UsuarioResponse {
  id: number
  nombre: string
  apellidos: string
  email: string
  ciudad: string
  created_at: string
}

// La respuesta completa de la API
export interface ApiResponse {
  success: boolean
  message: string
  user?: UsuarioResponse
  errors?: Record<string, string[]>
  sheets_synced?: boolean
}

// Para manejar errores específicos de la API
export interface ApiError {
  success: boolean
  message: string
  errors?: Record<string, string[]>
}