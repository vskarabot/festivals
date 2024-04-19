import authentication from "~/composables/auth"

// redirect before switching to page if user not logged in
export default defineNuxtRouteMiddleware((context) => {
    const { access } = authentication()
    if (!access.value) {
        return navigateTo('/auth/login')
    }
})