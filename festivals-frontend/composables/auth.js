export default function authentication() {
    const access = useCookie('access')
    const refresh = useCookie('refresh')

    const setTokens = (acc, ref) => {
        access.value = acc
        refresh.value = ref
    }

    const logout = () => {
        access.value = null
    }

    return {
        access,
        refresh,
        setTokens,
        logout
    }
}