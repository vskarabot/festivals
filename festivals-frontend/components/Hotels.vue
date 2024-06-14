<template>
    <div v-for="hotel in hotels" :key="hotel.name">
        <a :href="hotel.link" target="_blank">{{ hotel.name }}</a>
        Location: {{ hotel.location }}
        Distance from festival: {{ hotel.distance }}
        Price: {{ hotel.price }}
        Rating: {{ hotel.review[0] }}
        Number of reviews: {{ hotel.review[1] }}
    </div>
</template>

<script setup>
    const props = defineProps({
        hotels: {
            type: Object,
            required: true,
        },
    })
</script>