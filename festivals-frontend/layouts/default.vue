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
                                            :to="`/festivals/${notification.festival}/chats/${notification.chat}?message=${notification.message}`"
                                        >
                                            <v-card-text class="pb-0 mb-0"><b>{{ notification.chat_name }}</b> • {{ notification.time_string }}</v-card-text>
                                            <v-card-subtitle class="mb-4" :opacity="10">User <b>{{ notification.message_username }}</b> wrote: "{{ notification.message_text}}"</v-card-subtitle>
                                        </v-card>
                                    </v-col>
                                    <v-col cols="2">
                                        <v-icon icon="mdi-circle-medium" color="teal-lighten-1"></v-icon>
                                    </v-col>
                                </v-row>
                                <v-divider thickness="2"></v-divider>
                            </v-list-item>
                            <v-card class="py-2 text-center" rounded="0" color="secondary"><v-btn width="90%"color="teal-lighten-1" rounded="xl">See all</v-btn></v-card>  
                        </v-list>
                    </v-menu>
                </v-btn>

                <v-btn icon="mdi-forum" variant="plain" @click="forum"></v-btn>

                <!-- TODO : add some kind of menu to display also username and put next 2 v-btn into one -->
                <v-btn icon="mdi-account" variant="plain" @click="profile"></v-btn>

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

    const { logout, logedUser } = authentication()

    const menu = ref(false)

    const notificationsList = ref('')

    onMounted(async() => {
        notificationsList.value = await requests.getNotifications()
        console.log(notificationsList.value)
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

    const profile = () => {
        useRouter().push('/me/profile/')
    }

    const unreadNotifications = computed(() => {
        if (notificationsList && notificationsList.value.length) {
            return notificationsList.value.filter(notification => !notification.read).length
        }
    })

    const notifications = () => {
        
    }
</script>

<style scoped>
    .no-radius {
        border-radius: 0;
    }
</style>