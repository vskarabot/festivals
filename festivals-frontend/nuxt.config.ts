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
    '@/plugins/vuetify.ts'
  ],
  devtools: { enabled: true },
  modules: [
    'nuxt-mapbox'
  ],
  mapbox: {
    accessToken: 'pk.eyJ1IjoidnM3MDE1IiwiYSI6ImNsdmF4OXkxMDAzZmYyam52bHMzMXkzM2YifQ.COvY-tigswKIlF3DRqURfA'
  }
})
