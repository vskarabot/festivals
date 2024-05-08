// authentication data
import * as services from '../services/requests'

export default function authentication() {
    const access = useCookie('access')
    const refresh = useCookie('refresh')
    const logedUser = useCookie('user')

    // login function
    const setTokens = (acc, ref, usernameOrEmail) => {
        access.value = acc
        if (ref)
            refresh.value = ref
        if (usernameOrEmail)
            logedUser.value = usernameOrEmail
    }

    const logout = () => {
        access.value = null
        refresh.value = null
        logedUser.value = null
    }

    // Proactive authentication  (before each request)
    const isAuthenticated = async () => {

        // check if token is valid (verify)
        const tokenValid = await services.verifyToken()

        if (tokenValid !== 200) {
            // not valid , check if refresh is valid
            const refreshValid = await services.refreshToken()

            if (refreshValid !== 200) {
                // not valid, logout
                logout()
                
                // and also redirect
                return navigateTo('/auth/login')
            }   
        }
    }

    return {
        access,
        refresh,
        logedUser,
        setTokens,
        logout,
        isAuthenticated
    }
}