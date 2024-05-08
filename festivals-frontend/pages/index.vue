<template>
    <!-- sloted menu -->
    
    
    <div v-if="festivals">
        <h1>Home page</h1>
        Didn't find your festival? Create new community for the festival! <NuxtLink to="festivals/add-edit-festival">Add a festival</NuxtLink>

        <h2>List of "popular" festivals:</h2>
        <div v-for="festival in festivals">
            <NuxtLink :to="`/festivals/${festival.id}`">
                <p>{{ festival.name }}</p>
            </NuxtLink>
        </div>
    </div>
</template>

<script setup>
    import * as services from '../services/requests'

    const festivals = ref(null)

    onMounted(async () => {
        const response = await services.getFestivals()

        if (response.status === 200) {
            festivals.value = await response.json()
        }
    })
</script>