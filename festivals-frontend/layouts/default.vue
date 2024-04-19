<template>
    <!-- menu for now -->
    <div>
        <div>User: {{ logedUser }}</div>
        <NuxtLink to="/auth/login/" @click="handleLogout">Logout</NuxtLink>
        <hr>
    </div>
    <slot></slot>
</template>

<script setup>
    import authentication from '~/composables/auth'

    const { logout, access, logedUser } = authentication()

    const handleLogout = () => {
        logout()
    }
</script>