<template>
    <!-- sloted menu -->
    
    
    <div v-if="festivals">
        <h1>Home page</h1>
        Didn't find your festival? Create new community for the festival! <NuxtLink to="/add-festival">Add a festival</NuxtLink>

        <h2>List of "popular" festivals:</h2>
        <div v-for="festival in festivals">
            <NuxtLink :to="`/festivals/${festival.id}`">
                <p>{{ festival.name }}</p>
            </NuxtLink>
        </div>
    </div>
</template>

<script setup>
import authentication from '@/composables/auth'

const { access } = authentication()
const festivals = ref(null)

definePageMeta({
    middleware: 'logedin'
})

onMounted(async () => {
    const res = await fetch('http://localhost:8000/festivals/', {
        method: 'GET',
        headers: {
            'Authorization': `JWT ${access.value}`
        }                
    })

    if (res.status === 200) {
        festivals.value = await res.json()
    }

})
</script>