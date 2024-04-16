<template>
    <!-- menu for now -->
    <div>
        <NuxtLink to="/auth/login/" @click="handleLogout">Logout</NuxtLink>
        <hr>
    </div>
    <slot></slot>
</template>

<script setup>
    import authentication from '~/composables/auth'

    const { logout, access } = authentication()

    const handleLogout = () => {
        logout()
    }
</script>