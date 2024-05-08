// all requests to backend

import * as urls from '../constants/urls'
import authentication from '~/composables/auth'

/**
 * Authentication endpoints
 */

// VERIFY TOKEN
export const verifyToken = async () => {

    const { access } = authentication()

    const response = await fetch(urls.VERIFY, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            token: access.value
        })
    })

    // returns 200 if ok, 401 if field missing, 400 if token is invalid
    return response.status
}

// REFRESH TOKEN
export const refreshToken = async () => {

    const { refresh, setTokens } = authentication()

    const response = await fetch(urls.REFRESH, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            refresh: refresh.value
        })
    })

    // if valid it returns new access token -> set it
    if (response.status === 200) {
        const responseData = await response.json()
        setTokens(responseData.access)
    }

    return response.status
}


// REGISTER
export const register = async (data) => {
    const response = await fetch(urls.REGISTER, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            first_name: data.fName,
            last_name: data.lName,
            username: data.username,
            email: data.email,
            password: data.password,
            date_of_birth: data.birthDate,
            country: data.country,
            gender: data.selectedGender,
        })
    })

    // handle the logic (this weak now)
    const responseData = await response.json()

    if (responseData.id) {
        return true
    }
    // handle if it fails
}

// EMAIL ACTIVATION RESEND
export const resend = async (email) => {
    await fetch(urls.RESEND, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email
        })
    })
}

// LOGIN
export const login = async (data) => {
    const { setTokens } = authentication()

    const response = await fetch(urls.LOGIN, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: data.usernameOrEmail,
            password: data.password
        })
    })

    const responseData = await response.json()
    if (responseData.detail) {
        console.log(responseData.detail)
    }
    else {
        setTokens(responseData.access, responseData.refresh, data.usernameOrEmail)
        return navigateTo('/')
    }
}

// ACCOUNT ACTIVATION
export const activate = async (uid, token) => {
    const response = await fetch(urls.ACTIVATE, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            uid: uid,
            token: token
        })
    })

    return response      
}

// GET CURRENT USER
export const getCurrentUser = async () => {
    const { access } = authentication()

    const response = await fetch(urls.CURRENT_USER, {
        headers: {
            'Authorization': `JWT ${access.value}`
        }
    })

    return response
}

/**
 * FESTIVALS
 */

// MAYBE MAKE AUTHENTICATED FETCH TO REDUCE CODE DUPLICATION

// GET ALL FESTIVALS
export const getFestivals = async () => {
    
    // get only method as access can change if token is refreshed
    const { isAuthenticated } = authentication()
    await isAuthenticated()
    // now get the access as there is no possibility that it was changed in the meantime
    const { access } = authentication()

    const response = await fetch(urls.FESTIVALS, {
        method: 'GET',
        headers: {
            'Authorization': `JWT ${access.value}`
        }                
    })

    return response
}

// GET FESTIVAL DETAIL
export const getFestivalById = async (id) => {
    const { access } = authentication()

    const response = await fetch(urls.FESTIVAL_DETAIL(id), {
        method: 'GET',
        headers: {
            'Authorization': `JWT ${access.value}`
        }
    })

    return response
}

// CREATE NEW FESTIVAL
export const createFestival = async (data) => {
    const { access } = authentication()

    const response = await fetch(urls.FESTIVALS, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        },
        body: JSON.stringify({
            name: data.name,
            info: data.info,
            website: data.website,
            lat: data.lat,
            lon: data.lon,
        })
    })

    return response
}

// UPDATE (PUT) FESTIVAL
export const updateFestival = async (id, data) => {
    const { access } = authentication()

    const response = await fetch(urls.FESTIVAL_DETAIL(id), {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        },
        body: JSON.stringify({
            name: data.name,
            info: data.info,
            website: data.website,
            lat: data.lat,
            lon: data.lon,
        })
    })
    
    return response
}