<template>
    <v-chip
        class="mx-2 my-2"
        color="red"
        variant="elevated"
    >
        <v-icon v-if="festival.is_favourite" icon="mdi-heart" class="mr-2"/>
        <v-icon v-else icon="mdi-heart-outline" class="mr-2"/>
        {{ festival.num_favourites }}
    </v-chip>
</template>

<script setup>
    const props = defineProps({
        festival: Object
    })
</script>