// list of all urls used in the application backend
// format -> export const URL_NAME = 'url'; 
// also set base url like export const BASE_URL = 'http://localhost:8000';
// so then you can use it like `${BASE_URL}/...`

// BASE
export const BASE_URL = 'http://localhost:8000'

// USER AUTH
export const ACTIVATE = BASE_URL + '/auth/users/activation/'               // POST
export const LOGIN = BASE_URL + '/auth/jwt/create/'                        // POST
export const REGISTER = BASE_URL + '/auth/users/'                          // POST (and get?)
export const RESEND = BASE_URL + '/auth/users/resend_activation/'          // POST

// TOKEN
export const REFRESH = BASE_URL + '/auth/jwt/refresh/'                     // POST
export const VERIFY = BASE_URL + '/auth/jwt/verify/'                       // POST

// USER
export const CURRENT_USER = BASE_URL + '/auth/users/me/'                   // GET

// FESTIVAL
export const FESTIVALS = BASE_URL + '/festivals/'
export const FESTIVAL_DETAIL = (id) => BASE_URL + `/festivals/${id}`

// POSTS
export const POSTS = BASE_URL + `/posts/`
export const POST_DETAIL = (postId) => BASE_URL + `/posts/${postId}`

// CHATS
export const CHAT_DETAIL = (chatId) => BASE_URL + `/chats/${chatId}`
export const FESTIVAL_CHATS = (festivalId) => BASE_URL + `/festivals/${festivalId}/chats/`
export const MESSAGES = (festivalId, chatId) => BASE_URL + `/festivals/${festivalId}/chats/${chatId}`

// COMMENTS
export const POST_COMMENTS = (postId) => BASE_URL + `/posts/${postId}/comments`
export const DELETE_COMMENT = (commentId) => BASE_URL + `/comments/${commentId}`