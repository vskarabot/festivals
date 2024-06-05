<template>
    <!-- menu for now -->
    <div>
        <button @click="home">Home</button>
        <button @click="forum">News</button>
        <div>User: <NuxtLink to="/me/profile/">{{ logedUser }}</NuxtLink></div>
        <NuxtLink to="/auth/login/" @click="handleLogout">Logout</NuxtLink>
        <hr>
    </div>
    <slot></slot>
</template>

<script setup>
    import authentication from '~/composables/auth'

    const { logout, logedUser } = authentication()

    const handleLogout = () => {
        logout()
    }

    const home = () => {
        useRouter().replace('/')
    }

    const forum = () => {
        useRouter().replace(`/forum/`)
    }
</script>