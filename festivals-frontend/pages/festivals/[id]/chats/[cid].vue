<template>
    <v-sheet class="pa-4 mx-auto" max-width="500" width="100%">
        <v-card class="mx-auto">
            <v-sheet class="d-flex justify-space-between align-center" height="70" color="indigo-darken-4">
                <v-card-title>Chat</v-card-title>
                <v-icon v-if="notifications" class="pr-8" icon="mdi-bell" @click="notifications = false"></v-icon>
                <v-icon v-else class="pr-8" icon="mdi-bell-off" @click="notifications = true"></v-icon>
            </v-sheet>
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
        <v-textarea
            class="my-4"
            variant="outlined" 
            v-model="newMessage" 
            label="New message..."
            rounded="xl"
            rows="1"
            row-height="15"
            auto-grow
        >
            <template v-slot:prepend-inner>
                <v-btn
                    icon="mdi-emoticon"
                    :variant="emojiHover ? 'flat' : 'text'"
                    color="indigo-darken-4"
                    @mouseleave="emojiHover = false"
                    @mouseover="emojiHover = true"
                    @click=""
                ></v-btn>
            </template>
            <template v-slot:append-inner>
                <v-btn
                    icon="mdi-send"
                    variant="plain"
                    :color="sendHover ? 'primary' : ''"
                    @mouseleave="sendHover = false"
                    @mouseover="sendHover = true"
                    @click="sendMessage"
                ></v-btn>
            </template>
        </v-textarea>
    </v-sheet>

</template>
  
<script setup>
    import { ref, onMounted } from 'vue'
    import * as requests from '../../services/requests'
    import { useRoute } from 'vue-router'

    import Pusher from 'pusher-js'  

    const emojiHover = ref(false)
    const sendHover = ref(false)

    const infiniteScroll = ref(null)    
    const apiMessages = ref([])
    const nextPage = ref('Initial')
    const newMessage = ref('')

    const notifications = ref(false)
    
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
        // Pusher for new messages          
        const pusher = new Pusher('e08dbedd3b10916330c8', {
            cluster: 'eu',
        })            
        const channel = pusher.subscribe(`chat-${chatId}`);        
        // Subscribe to the channel and bind to events -> channel chat-{chatId} and event new-message
        channel.bind('new-message', (data) => {
            // push live messages to the messages array
            const container = infiniteScroll.value.$el
            let scroll = false
            // only scroll to bottom if we are at the bottom
            // scrollHeight -> height of whole infinite scroll; scrollTop -> from visible top to top of infinite scroll; clientHeight -> visible height
            if (container.scrollHeight - container.scrollTop === container.clientHeight)
                scroll = true
            apiMessages.value.push(data)

            if (scroll) {
                nextTick(() => {
                    container.scrollTop = container.scrollHeight
                })
            }
        })

        onBeforeRouteLeave(() => {
            pusher.disconnect()
        })
    })

    onActivated(async () => {
        const container = infiniteScroll.value.$el
        container.scrollTop = container.scrollHeight       
    })

    const sendMessage = () => {
        // Send message to API
        requests.sendMessage(festivalId, chatId, newMessage.value)
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

</script>
  