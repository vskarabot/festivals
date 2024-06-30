<template>

    <v-sheet class="pa-4 mx-auto" max-width="500" width="100%">
        <v-card class="mx-auto pl-8 py-8">
            <v-card-title>
                CHAT NAME
            </v-card-title>
            <v-divider></v-divider>
            <v-infinite-scroll ref="infiniteScroll" :items="apiMessages" :onLoad="load" side="start" height="500">
                <div v-for="message in apiMessages" :key="message">
                    <Message :message="message" />
                </div>
                <template v-slot:empty>
                    <!-- to not show message if no messages left -->
                </template>
            </v-infinite-scroll>
        </v-card>
        <v-text-field
            class="my-4"
            type="text" 
            variant="outlined" 
            v-model="newMessage" 
            label="New message"
            appendInnerIcon="mdi-send" 
            prependIcon="mdi-emoticon"
        />
    </v-sheet>

</template>
  
<script setup>
    import { ref, onMounted } from 'vue'
    import * as requests from '../../services/requests'
    import authentication from '~/composables/auth'

    const { userId } = authentication()

    // Pusher for new messages
    import Pusher from 'pusher-js'    
    import { useRoute } from 'vue-router';
    /*const pusher = new Pusher('e08dbedd3b10916330c8', {
        cluster: 'eu',
    })

    inject('pusher', pusher)*/

    const infiniteScroll = ref(null)
    
    const apiMessages = ref([])
    const nextPage = ref('Initial')
    const newMessage = ref('')
    
    // Get chat ID and author ID from props
    const festivalId = useRoute().params.id
    const chatId = useRoute().params.cid

    // check if exists
    const { error } = await useFetch(`http://localhost:8000/festivals/${festivalId}/chats/${chatId}`)
    if (error.value) {
    // Simple error handling.
        throw createError({ statusCode: error.value?.statusCode, statusMessage: error.value?.statusMessage, fatal: true })
    }
    
    onMounted(async() => {
         
        // Subscribe to the channel and bind to events -> channel chat-{chatId} and event new-message
        /*
        const channel = pusher.subscribe(`chat-${chatId}`);
        channel.bind('new-message', (data) => {
            // push live messages to the messages array

            // TODO here change console log to data.is_author = ...
            if (userId.value === data.author_id) {
                console.log(true)
            } else {
                console.log(false)
            }
            
            // TODO : we need to add to begining not the end
            apiMessages.value.push(data)
        })*/

    })

    const sendMessage = () => {
        // Send message to API
        //requests.sendMessage(festivalId, chatId, newMessage.value)
        newMessage.value = ''
    }

    const load = async({ done }) => {
        // initial load
        if (nextPage.value) {
            let response
            if (nextPage.value === 'Initial') {
                response = await requests.getInitialMessages(festivalId, chatId)
            }
            else {
                response = await requests.getMoreMessages(nextPage.value)
            }
            const responseData = await response.json()              
            nextPage.value = responseData.next
            apiMessages.value.unshift(...responseData.results.reverse())
            done('ok')
        }
        else {
            done('empty')
        }
    }

    const scrollToBottom = () => {
        const container = infiniteScroll.value.$el
        container.scrollTop = container.scrollHeight
    }

    // works perfectly as when the page opens load won't trigger as it's set to bottom
    // we won't have a problem loading unecesary data as we would else
    onActivated(() => {
        scrollToBottom()
    })

</script>
  