import Pusher from 'pusher-js'

export default defineNuxtPlugin(nuxtApp => {
    const pusher = new Pusher('e08dbedd3b10916330c8', {
        cluster: 'eu'
    })

    nuxtApp.provide('pusher', pusher)
})