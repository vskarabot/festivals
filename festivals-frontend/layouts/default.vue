<template>
    <v-card>
        <v-layout>
            <v-app-bar prominent>
                <v-toolbar-title><v-btn @click="home"><b>Fest</b></v-btn></v-toolbar-title>

                <v-spacer></v-spacer>

                <v-btn icon="mdi-forum" variant="text" @click="forum"></v-btn>

                <v-btn icon="mdi-bell" variant="text"></v-btn>

                <!-- TODO : add some kind of menu to display also username and put next 2 v-btn into one -->
                <v-btn icon="mdi-account" variant="text" @click="profile"></v-btn>

                <v-btn icon="mdi-logout" variant="text" @click="handleLogout"></v-btn>

            </v-app-bar>

            <v-main>
                <slot></slot>
            </v-main>
        </v-layout>
    </v-card>
</template>

<script setup>
    import authentication from '~/composables/auth'

    const { logout, logedUser } = authentication()

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
</script>