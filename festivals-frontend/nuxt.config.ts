import vuetify, { transformAssetUrls } from "vite-plugin-vuetify"

export default defineNuxtConfig({
  css: [
    'vuetify/lib/styles/main.sass',
    '@mdi/font/css/materialdesignicons.min.css',
  ],
  build: {
    transpile: ['vuetify'],
  },
  plugins: [
    '@/plugins/vuetify.ts',
    '@/plugins/firebase.ts',
    '@/plugins/pusher.ts',
  ],
  extends: [
    'nuxt-emoji'
  ],
  devtools: { enabled: true },
  modules: [
    'nuxt-mapbox'
  ],
  runtimeConfig: {
    public: {
      mapboxToken: process.env.MAPBOX_TOKEN
    }
  }
})
