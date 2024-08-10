<template>
    <v-icon icon="mdi-map-marker"></v-icon>
    <v-card-subtitle class="pb-4">
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
    
    const addressLength = mbLoc?.features[0]?.context?.length
    locationName.value = mbLoc.features[0].text + ", " + mbLoc.features[0]?.context[addressLength - 1]?.text
</script>