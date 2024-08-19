import Pusher from 'pusher-js'

export default defineNuxtPlugin(nuxtApp => {
    const pusherKey = useRuntimeConfig().public.pusherKey
    const pusher = new Pusher(pusherKey, {
        cluster: 'eu'
    })

    nuxtApp.provide('pusher', pusher)
})