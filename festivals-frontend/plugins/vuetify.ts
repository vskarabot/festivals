import { createVuetify } from 'vuetify'
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

export default defineNuxtPlugin((nuxtApp) => {
    const vuetify = createVuetify({
        ssr: true,
        components,
        directives,
        theme: { 
            defaultTheme: 'dark',
            themes: {
                dark: {
                    dark: true,
                    colors: {
                        primary: '#0a0f21',
                        secondary: '#232C4C',
                        card: '#4B5476'
                    }
                }
            }
        }
    })
    nuxtApp.vueApp.use(vuetify)
})
