// authentication data
import * as requests from '../services/requests'

export default function authentication() {
    const access = useCookie('access')
    const refresh = useCookie('refresh')
    const logedUser = useCookie('user')
    const userId = useCookie('userId')

    // login function
    const setTokens = async (acc, ref) => {
        access.value = acc
        if (ref)
            refresh.value = ref
        
        // set data for user
        const response = await requests.getCurrentUser()
        const responseData = await response.json()
        
        // TODO handle if something wrong

        // add to cookies user data
        logedUser.value = responseData.username
        userId.value = responseData.id
    }

    const logout = () => {
        access.value = null
        refresh.value = null
        logedUser.value = null
        userId.value = null
    }

    // Proactive authentication  (before each request)
    const isAuthenticated = async () => {
  
        // check if token is valid (verify)
        const tokenValid = await requests.verifyToken()

        if (tokenValid !== 200) {
            // not valid , check if refresh is valid
            const refreshValid = await requests.refreshToken()

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
        userId,
        setTokens,
        logout,
        isAuthenticated
    }
}