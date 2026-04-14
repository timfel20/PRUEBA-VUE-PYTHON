// nuxt.config.ts
export default defineNuxtConfig({
  devtools: { enabled: true },
  
  modules: ['@nuxtjs/tailwindcss'],
  
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api'
    }
  },
  
  // Nuxt 4 specific - tell it where your app folder is
  dir: {
    app: 'app'
  },
  
  typescript: {
    strict: true
  },
  
  // Enable Nuxt 4 compatibility
  future: {
    compatibilityVersion: 4
  }
})