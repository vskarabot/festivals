<template>
    <v-sheet color="primary" class="py-8">
        <v-card class="mx-auto" max-width="500" rounded="xl" color="card">
            <v-sheet class="d-flex justify-space-between align-center" height="70" color="secondary">
                <v-card-title v-if="chatDetails && chatDetails.name">{{ chatDetails.name }}</v-card-title>
                <v-progress-circular v-else></v-progress-circular>
                <v-icon v-if="chatDetails.notify_user" color="teall1" class="pr-8" icon="mdi-bell" @click="manageNotifications"></v-icon>
                <v-icon v-else class="pr-8" color="teall1" icon="mdi-bell-off" @click="manageNotifications"></v-icon>
            </v-sheet>
            
            <v-divider thickness="3" color="primary" opacity="10"></v-divider>
            
            <v-infinite-scroll ref="infiniteScroll" :items="apiMessages" :onLoad="load" side="start" height="500" @scroll.native="scrolling">
                <div v-for="(message, index) in apiMessages" :key="message.id" :id="'message-' + message.id">

                    <v-divider v-if="showDivider(index)" class="mx-4" color="teall1" opacity="10" inset :thickness="1">New messages</v-divider>

                    <Message :message="message" />
                </div>
                <template v-slot:empty>
                    <v-card-text>No more messages...</v-card-text>
                </template>
                <v-btn
                    v-if="showDownButton"
                    @click="scrollToBottom"
                    icon="mdi-chevron-down"
                    size="small"
                    color="teall1"
                    class="position-absolute mb-4 scroll-down-style"
                >
                </v-btn> 
            </v-infinite-scroll>
        </v-card>
        <!-- text input -->
        <v-textarea
            max-width="500"
            class="mx-auto my-4"
            color="teall1"
            variant="outlined" 
            v-model="newMessage" 
            label="New message..."
            rounded="xl"
            rows="1"
            row-height="15"
            auto-grow
            @keyup.enter="sendMessage"
        >
            <template v-slot:prepend-inner>
                <v-btn
                    icon="mdi-emoticon"
                    variant="plain"
                    :color="emojiHover ? 'yellow': 'teall1'"
                    @mouseleave="emojiHover = false"
                    @mouseover="emojiHover = true"
                    @click=""
                ></v-btn>
            </template>
            <template v-slot:append-inner>
                <v-btn
                    icon="mdi-send"
                    variant="plain"
                    color="teall1"
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

    // ref for infinite scroll
    const infiniteScroll = ref(null)
    const heightValues = ref(
        { scrollHeight: 0 },
        { scrollTop: 0 },
        { clientHeight: 0 }
    )

    const apiMessages = ref([])
    const nextPage = ref('Initial')
    const newMessage = ref('')

    // Get chat ID and author ID from props
    const festivalId = useRoute().params.id
    const chatId = useRoute().params.cid
    const chatDetails = ref('')

    // access from notifications
    const newMessageId = ref(parseInt(useRoute().query.message))

    // check if exists
    const { error } = await useFetch(`http://localhost:8000/festivals/${festivalId}/chats/${chatId}`)
    if (error.value) {
    // Simple error handling.
        throw createError({ statusCode: error.value?.statusCode, statusMessage: error.value?.statusMessage, fatal: true })
    }
    
    onMounted(async() => {
        // fetch chat details (will also return if user should get notification as notify_user)
        chatDetails.value = await requests.chatDetails1(festivalId, chatId)
        
        // Pusher for new messages          
        const pusher = new Pusher('e08dbedd3b10916330c8', {
            cluster: 'eu',
        })            
        const channel = pusher.subscribe(`chat-${chatId}`);        
        // Subscribe to the channel and bind to events -> channel chat-{chatId} and event new-message
        channel.bind('new-message', (data) => {
            // push live messages to the messages array
            apiMessages.value.push(data)
            
            nextTick (() => {
                const element = infiniteScroll?.value.$el
                heightValues.value.scrollHeight = element.scrollHeight
                heightValues.value.scrollTop = element.scrollTop
                heightValues.value.clientHeight= element.clientHeight
            })
        })

        jumpToMessage()

        onBeforeRouteLeave(() => {
            pusher.disconnect()
        })
    })

    onActivated(async () => {        
        jumpToMessage()
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

    const manageNotifications = async() => {
        const response = await requests.manageNotifications(festivalId, chatDetails.value.id, !chatDetails.value.notify_user)
        console.log(response)
        chatDetails.value = response
    }

    const jumpToMessage = () => {
        nextTick (() => {
            if (newMessageId.value) {
                const messageElement = document.getElementById('message-'+ newMessageId.value)
                if (messageElement) {
                    messageElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
                }
            }
        })
    }

    const showDivider = (index) => {
        return apiMessages.value[index].id === newMessageId.value
    }

    const scrolling = (event) => {
        const element = event.target
        heightValues.value.scrollHeight = element.scrollHeight
        heightValues.value.scrollTop = element.scrollTop
        heightValues.value.clientHeight= element.clientHeight
    }

    const showDownButton = computed(() => {
        return heightValues.value.scrollHeight - heightValues.value.scrollTop !== heightValues.value.clientHeight
    })

    const scrollToBottom = () => {
        const container = infiniteScroll.value.$el
        container.scrollTo({
            top: container.scrollHeight,
            behavior: 'smooth'
        })  
    }
</script>

<style>
    .scroll-down-style {
        left: 50%;
        bottom: 0;
        transform: translate(-50%);
    }
</style>
  