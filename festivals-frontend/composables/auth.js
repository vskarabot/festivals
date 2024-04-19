// authentication data

export default function authentication() {
    const access = useCookie('access')
    const refresh = useCookie('refresh')
    const logedUser = useCookie('user')

    // login function
    const setTokens = (acc, ref, usernameOrEmail) => {
        access.value = acc
        refresh.value = ref
        logedUser.value = usernameOrEmail
    }

    const logout = () => {
        access.value = null
        refresh.value = null
        logedUser.value = null
    }

    return {
        access,
        refresh,
        logedUser,
        setTokens,
        logout
    }
}