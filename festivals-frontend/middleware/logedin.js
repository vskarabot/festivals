import authentication from "~/composables/auth"

export default defineNuxtRouteMiddleware((context) => {
    const { access } = authentication()
    if (!access.value) {
        return navigateTo('/auth/login')
    }
})