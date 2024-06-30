import authentication from "~/composables/auth"

// to import in script setup:
/*definePageMeta({
    middleware: 'logedin'
})*/

// THIS PROBABLY WONT BE NEEDED BUT ILL LEAVE IT HERE FOR NOW
// redirect before switching to page if user not logged in

// TODO -> REIMPLEMENT IT!!!! NOT IMPLEMENTED
export default defineNuxtRouteMiddleware((context) => {
    const { access } = authentication()
    if (!access.value) {
        return navigateTo('/auth/login')
    }
})