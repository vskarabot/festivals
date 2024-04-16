<template>
    <div>
        <form @submit.prevent="login">
            <input type="text" placeholder="Username or email" v-model="usernameOrEmail"></input>
            <input type="password" placeholder="Password" v-model="password"></input>
            <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <NuxtLink to="/auth/register">Register</NuxtLink></p>
    </div>
</template>

<script setup>
import authentication from '~/composables/auth';

    definePageMeta({
        layout: 'blank'
    })

    const { setTokens } = authentication()
    
    const usernameOrEmail = ref('')
    const password = ref('')

    const login = async () => {
        const res = await fetch('http://localhost:8000/auth/jwt/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: usernameOrEmail.value,
                password: password.value
            })
        })

        const data = await res.json()                
        if (data.detail) {
            console.log(data.detail)
        }
        else {
            setTokens(data.access, data.refresh)
            return navigateTo('/')
        }
    }
</script>

