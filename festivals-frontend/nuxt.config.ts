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
      mapboxToken: process.env.MAPBOX_TOKEN,
      pusherKey: process.env.PUSHER_KEY,
      // firebase
      apiKey: process.env.API_KEY,
      authDomain: process.env.AUTH_DOMAIN,
      projectId: process.env.PROJECT_ID,
      storageBucket: process.env.STORAGE_BUCKET,
      messagingSenderId: process.env.MESSAGING_SENDER_ID,
      appId: process.env.APP_ID,
      measurementId: process.env.MEASUREMENT_ID
    }
  }
})
