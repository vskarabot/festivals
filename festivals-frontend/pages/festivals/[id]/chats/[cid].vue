<!-- components/Chat.vue -->

<template>
    <div>{{ apiMessages }}</div>
    <input type="text" v-model="newMessage" placeholder="Type your message here"><button @click="sendMessage">Send</button>
</template>
  
<script setup>
    import { ref, onMounted } from 'vue'
    import * as requests from '../../services/requests'
    import authentication from '~/composables/auth'

    const { userId } = authentication()

    // Pusher for new messages
    import Pusher from 'pusher-js'    
    import { useRoute } from 'vue-router';
    const pusher = new Pusher('e08dbedd3b10916330c8', {
        cluster: 'eu',
    })

    inject('pusher', pusher)

    
    const apiMessages = ref([])
    const newMessage = ref('')
    
    // Get chat ID and author ID from props
    const festivalId = useRoute().params.id
    const chatId = useRoute().params.cid
    
    onMounted(async() => {
        // Subscribe to the channel and bind to events -> channel chat-{chatId} and event new-message
        const channel = pusher.subscribe(`chat-${chatId}`);
        channel.bind('new-message', (data) => {
            // push live messages to the messages array

            // TODO here change console log to data.is_author = ...
            if (userId.value === data.author_id) {
                console.log(true)
            } else {
                console.log(false)
            }
            
            apiMessages.value.push(data)
        })

        // Fetch messages from the API
        const response = await requests.getMessages(festivalId, chatId)
        console.log(response)
        const responseData = await response.json()
        apiMessages.value = responseData
    })

    const sendMessage = () => {
        // Send message to API
        requests.sendMessage(festivalId, chatId, newMessage.value)
    }
</script>
  