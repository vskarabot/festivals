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
    try {
        const response = await $fetch(urls.REGISTER, {
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
                gender: data.selectedGender
            }),
            ignoreResponseError: true
        })

        return response
    } catch (error) {
        return error.data ?? error
    }
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
        setTokens(responseData.access, responseData.refresh)
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

    const { isAuthenticated } = authentication()
    await isAuthenticated()    
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
export const getFestivals = async (search) => {

    // get only method as access can change if token is refreshed
    const { isAuthenticated, access } = authentication()
    await isAuthenticated()

    // IMPORTATN if it fails you know the problem ˇ
    // as navigateTo triggers new page load, code from here is not executed if auth.js logs out
    // now get the access as there is no possibility that it was changed in the meantime
    // const { access } = authentication()
 
    let url = urls.FESTIVALS
    if (search)
        url += search

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': `JWT ${access.value}`
        }                
    })

    return response
}

// GET FESTIVAL DETAIL
export const getFestivalById = async (id) => {

    const { isAuthenticated } = authentication()
    await isAuthenticated()

    const { access } = authentication()

    const response = await fetch(urls.FESTIVAL_DETAIL(id), {
        method: 'GET',
        headers: {
            'Authorization': `JWT ${access.value}`
        }
    })

    return response
}

// HOTELS ENDPOINT IS NOT SET IN URLS AND NOT IMPLEMENTED HERE
// I JUST USED IT IN INDEX.vue

// CREATE NEW FESTIVAL
export const createFestival = async (data) => {

    const { isAuthenticated } = authentication()
    await isAuthenticated()

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
            date_start: data.date_start,
            date_end: data.date_end,
            img: data.img
        })
    })

    return response
}

// UPDATE (PUT) FESTIVAL - drf handles partial updates by itself
export const updateFestival = async (id, data) => {

    const { isAuthenticated } = authentication()
    await isAuthenticated()

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
            date_start: data.date_start,
            date_end: data.date_end,
            img: data.img
        })
    })
    
    return response
}


// ADD TO FAVOURITES (same endpoint as update) -- FIIXXX THISSS
export const addToFavourites = async (festivalId) => {

    const { isAuthenticated } = authentication()
    await isAuthenticated()
    const { access } = authentication()

    const response = await fetch(urls.FESTIVAL_DETAIL(festivalId), {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        },
        body: JSON.stringify({
            favourite: true
        })
    })

    return response
}


// GET POSTS - > filtering available
export const getPosts = async (festivalId, params) => {

    const { isAuthenticated } = authentication()
    await isAuthenticated()
    const { access } = authentication()

    // for filtering by festival
    let url = urls.POSTS
    if (festivalId) {
        url += `?festival=${festivalId}&`
    }
    
    url += params

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        },
    })

    return response
}

// GET POST DETAIL
export const getPostDetail = async (postId) => {

    const { isAuthenticated } = authentication()
    await isAuthenticated()
    const { access } = authentication()

    const response = await fetch(urls.POST_DETAIL(postId), {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        }
    })

    return response

}


// ADD POST
export const addPost = async (festivalId, post) => {

    const { isAuthenticated } = authentication()
    await isAuthenticated()
    const { access } = authentication()

    const response = await fetch(urls.POSTS, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        },
        body: JSON.stringify({
            festival: festivalId,
            title: post.title,
            text: post.text,
            label: post.label,
        })
    })

    return response
}

// LIKE/DISLIKE POST
export const likePost = async(postId, action) => {
    
    const { isAuthenticated } = authentication()
    await isAuthenticated()
    const { access } = authentication()

    const response = await fetch(urls.POST_DETAIL(postId), {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        },
        body: JSON.stringify({
            'action': action
        })
    })

    return response
}

// DELETE OWN POST
export const deletePost = async(postId) => {

    const { isAuthenticated } = authentication()
    await isAuthenticated()
    const { access } = authentication()

    const response = await fetch(urls.POST_DETAIL(postId), {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        }
    })

    return response
}

// EDIT POST
export const editPost = async (festival, postId, data) => {

    const { isAuthenticated } = authentication()
    await isAuthenticated()
    const { access } = authentication()

    const response = await fetch(urls.POST_DETAIL(postId), {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        },
        body: JSON.stringify({
            festival: festival,
            title: data.title,
            text: data.text,
            label: data.label
        })
    })

    return response

}



// CHATS GET
export const getChats = async(festivalId) => {

    const { isAuthenticated } = authentication()
    await isAuthenticated()
    const { access } = authentication()

    const response = await fetch(urls.FESTIVAL_CHATS(festivalId), {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        },
    })

    return response

}

// CHAT GET DETAILS
export const chatDetails = async(chatId) => {

    const { isAuthenticated } = authentication()
    await isAuthenticated()
    const { access } = authentication()

    const response = await fetch(urls.CHAT_DETAIL(chatId), {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        },
    })

    return response

}

// ADD CHAT
export const addChat = async(festivalId, chatName) => {
    
        const { isAuthenticated } = authentication()
        await isAuthenticated()
        const { access } = authentication()
    
        const response = await fetch(urls.FESTIVAL_CHATS(festivalId), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `JWT ${access.value}`
            },
            body: JSON.stringify({
                name: chatName
            })
        })

        return response
}

// MESSAGES GET (api)
export const getInitialMessages = async(festivalId, chatId) => {

    const { isAuthenticated } = authentication()
    await isAuthenticated()
    const { access } = authentication()

    const response = await fetch(urls.MESSAGES(festivalId, chatId), {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        },
    })

    return response
}

// LOAD MORE MESSAGES
export const getMoreMessages = async(url) => {

    const { isAuthenticated } = authentication()
    await isAuthenticated()
    const { access } = authentication()

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        },
    })

    return response
}

// SEND MESSAGE
export const sendMessage = async(festivalId, chatId, message) => {
    
        const { isAuthenticated } = authentication()
        await isAuthenticated()
        const { access } = authentication()
    
        const response = await fetch(urls.MESSAGES(festivalId, chatId), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `JWT ${access.value}`
            },
            body: JSON.stringify({
                text: message
            })
        })

        return response
}


// COMMENTS
// GET
export const getComments = async(postId, params)  => {

    const { isAuthenticated } = authentication()
    await isAuthenticated()
    const { access } = authentication()

    const url = urls.POST_COMMENTS(postId) + params

    const response = await $fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        }
    })

    return response
}

// ADD LEVEL 1 COMMENT if only postId, text
// ADD LEVEL x if also parent
export const addComment = async (postId, text, parent) => {

    const { isAuthenticated } = authentication()
    await isAuthenticated()
    const { access } = authentication()

    const body = {post: postId, text: text}
    if (parent) {
        body.parent = parent
    }

    const response = await fetch(urls.POST_COMMENTS(postId), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        },
        body: JSON.stringify(body)
    })

    return response
}

// "DELETE" COMMENT -> actually update the value to deleted=true, so we can still display replied comments
export const quazyDeleteComment = async (commentId) => {

    const { isAuthenticated } = authentication()
    await isAuthenticated()
    const { access } = authentication()

    const response = await fetch(urls.DELETE_COMMENT(commentId), {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        },
        body: JSON.stringify({
            deleted: true
        })
    })

    return response
}

// LIKE/DISLIKE COMMENT
export const likeComment = async(commentId, action) => {
    
    const { isAuthenticated } = authentication()
    await isAuthenticated()
    const { access } = authentication()

    const response = await fetch(urls.DELETE_COMMENT(commentId), {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${access.value}`
        },
        body: JSON.stringify({
            'action': action
        })
    })

    return response
}