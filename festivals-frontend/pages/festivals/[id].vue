<template>
    <p>This is details page for festival with id {{ id }}</p>
    <button>Add to favorites</button>
    <button>Go to festival forum</button>
    <p>{{ festival }}</p>
    <h2>{{ festival.name }}</h2>
    <p>Info: {{ festival.info }}</p>
    <p>Website: <a :href="festival.website">{{ festival.website }}</a></p>
    <p>Latitude: {{ festival.lat }}</p>
    <p>Longitude: {{ festival.lon }}</p>
    <hr>
    <p>ˇˇWe'll also implement maps here</p>
    <span>First map is for path. Second for choosing sleeping options nearby with parameters.</span>
</template>

<script setup>
    const { id } = useRoute().params
    const { data: festival } = await useFetch(`http://localhost:8000/festivals/${id}`)
</script>