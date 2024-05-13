<template>
    <div>{{ userData }}</div>
</template>

<script setup>
    import { onMounted } from 'vue';
    import * as services from '../../services/requests'

    const userData = ref('')

    onMounted(async () => {
        const response = await services.getCurrentUser()
        userData.value = await response.json()
    })
</script>