<template>
    <v-sheet
        class="pa-4 text-center mx-auto"
        max-width="600"
        rounded="lg"
        width="100%"
    >
        <v-card class="mx-auto px-8 py-8">
            <h1>Welcome!</h1>
            <br>
            <v-form @submit.prevent="login">
                <v-text-field v-model="credentials.usernameOrEmail" label="Username or email" clearable variant="outlined"></v-text-field>
                <v-text-field type="password" v-model="credentials.password" label="Password" clearable variant="outlined"></v-text-field>
                <v-btn type="submit" color="primary" class="d-block mx-auto">LOGIN</v-btn>

                <br>
                <p class="text-center">Don't have an account? <NuxtLink to="/auth/register">Sign-in</NuxtLink></p>
            </v-form>
        </v-card>
    </v-sheet>
</template>

<script setup>
definePageMeta({
    layout: 'blank'
})
import * as requests from '../services/requests'
    
    const credentials = ref({
        usernameOrEmail: '',
        password: ''
    })

    // responseData only if error i think
    const login = async () => {
        if (credentials.value.password && credentials.value.password) {
            const responseData = await requests.login(credentials.value)
        }
    }
</script>

