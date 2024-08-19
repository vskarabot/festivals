<template>
    <v-card>
        <v-layout>
            <v-app-bar elevation="5" prominent color="primary">
                <v-toolbar-title><v-btn @click="home" variant="plain"><b>Fest</b></v-btn></v-toolbar-title>

                <v-spacer></v-spacer>
                
                <v-btn variant="plain" stacked @click="notifications">
                    <v-badge v-if="unreadNotifications" color="error" :content="unreadNotifications">
                        <v-icon icon="mdi-bell"></v-icon>
                    </v-badge>
                    <v-badge v-else color="primary" :content="0">
                        <v-icon icon="mdi-bell"></v-icon>
                    </v-badge>
                    <v-menu v-model="menu" width="300" activator="parent" transition="scale-transition">
                        <v-list class="py-0 my-0 text-right">
                            <v-card color="secondary" rounded="0">
                                <v-row class="d-flex justify-space-between">
                                    <v-col class="text-left">
                                        <v-card-text><b>Notifications</b></v-card-text>
                                    </v-col>
                                    <v-col>
                                        <v-card-text><v-icon icon="mdi-close" @click="menu = false"></v-icon></v-card-text>
                                    </v-col>
                                </v-row>
                            </v-card>
                            <v-list-item
                                v-for="(notification, index) in notificationsList"
                                :key="index"
                                :value="notification"
                                class="px-0 py-0 text-left"
                            >
                                <v-row class="d-flex align-center" style="background-color: #4B5476;"><!-- same color as card -->
                                    <v-col cols="10">
                                        <v-card
                                            color="card"
                                            variant="flat"
                                            class="no-radius" 
                                            @click="openNotification(notification[0].festival, notification[0].chat, notification.slice(-1)[0].message)"
                                        >

                                            <v-card-text><b style="color: #0a0f21;">{{ notification[0].chat_name }}</b> ({{ formattedTime(notification[0].timestamp) }})</v-card-text>

                                            <v-divider thickness="1" opacity="10" color="primary"></v-divider>
                                            <v-card-text>You have <b style="color: #0a0f21;">{{ notification.length }}</b> new messages!</v-card-text>
                                        </v-card>
                                    </v-col>
                                    <v-col cols="2">
                                        <v-icon icon="mdi-circle-medium" color="teal-lighten-1"></v-icon>
                                    </v-col>
                                </v-row>
                                <v-divider thickness="3" opacity="10" color="primary"></v-divider>
                            </v-list-item>
                            <v-card class="py-2 text-center" rounded="0" color="secondary"><v-btn width="90%"color="teal-lighten-1" rounded="xl">See all</v-btn></v-card>  
                        </v-list>
                    </v-menu>
                </v-btn>

                <v-btn icon="mdi-forum" variant="plain" @click="forum"></v-btn>

                <v-btn icon="mdi-logout" variant="plain" @click="handleLogout"></v-btn>
            </v-app-bar>

            <v-main>
                <v-divider></v-divider>
                <slot></slot>
            </v-main>
        </v-layout>
    </v-card>
</template>

<script setup>
    import authentication from '~/composables/auth'
    import * as requests from '../services/requests'

    const { logout, userId } = authentication()

    const menu = ref(false)

    const notifications = ref(false)
    const notificationsList = ref('')

    onMounted(async() => {
        notificationsList.value = await requests.getNotifications()
        sortNotificationsByChat()

        const channel = useNuxtApp().$pusher.subscribe(`user-${userId.value}`)          
        // Subscribe to the channel and bind to events -> channel chat-{chatId} and event new-message
        channel.bind('notification', async(data) => {
            notificationsList.value = await requests.getNotifications()
            sortNotificationsByChat()
        })
        channel.bind('new-notification-enabled', async(data) => {
            notificationsList.value = await requests.getNotifications()
            sortNotificationsByChat()
        })
    })

    const handleLogout = () => {
        logout()
        useRouter().replace('/auth/login/')
    }

    const home = () => {
        useRouter().replace('/')
    }

    const forum = () => {
        useRouter().replace('/forum/')
    }

    const unreadNotifications = computed(() => {
        if (notificationsList.value) {
            return Object.keys(notificationsList.value).length
        }
    })

    const sortNotificationsByChat = () => {
        const items = notificationsList.value

        const notifs = {}

        items.forEach((notification) => {
            let temp = String(notification.chat)
            if (!notifs[temp]) {
                notifs[temp] = []
            }
            notifs[temp].push(notification)
        })
        
        notificationsList.value = notifs
    }

    const formattedTime = (timestamp) => {
        const { formatTimeDifference } = chatTimes()
        return formatTimeDifference(timestamp)
    }

    const openNotification = (fest, chat, lastMessage) => {
        useRouter().push(`/festivals/${fest}/chats/${chat}?message=${lastMessage}`)
    }
</script>

<style scoped>
    .no-radius {
        border-radius: 0;
    }
</style>