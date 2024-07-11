<template>
    <v-card-subtitle>
        {{ locationName }}
    </v-card-subtitle>
</template>

<script setup>
    const runtimeConfig = useRuntimeConfig()
    
    const props = defineProps({
        festival: Object
    })

    const locationName = ref('')

    const mbLoc = await $fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${props.festival.lon},${props.festival.lat}.json?access_token=${runtimeConfig.public.mapboxToken}`)
    locationName.value = mbLoc.features?.[0]?.place_name?.split(" ")?.slice(-1)[0]
</script>