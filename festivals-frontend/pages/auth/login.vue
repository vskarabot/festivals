<template>
    <div>
        <form @submit.prevent="login">
            <input type="text" placeholder="Username or email" v-model="credentials.usernameOrEmail"></input>
            <input type="password" placeholder="Password" v-model="credentials.password"></input>
            <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <NuxtLink to="/auth/register">Register</NuxtLink></p>
    </div>
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
        const responseData = await requests.login(credentials.value)
    }
</script>

