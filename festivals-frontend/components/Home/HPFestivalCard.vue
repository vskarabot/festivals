<template>
    <v-card
        v-for="(festival, index) in festivals" 
        :key="festival.id"
        class="mx-auto my-2"
        max-width="570"
        elevation="2"
        color="secondary"
        variant="flat"
        @click=""
    >
        <v-sheet
            v-if="festival.img === 'error'"
            color="secondary"
            class="text-left"
            variant="text"
        >
            <HomeFavouriteBy :festival="festival" />
            
            <v-tooltip text="Image not found">
                <template v-slot:activator="{ props }">
                    <v-icon v-bind="props" icon="mdi-image-broken"></v-icon>
                </template>
            </v-tooltip>
        </v-sheet>
        <v-img
            v-else-if="festival.img"
            class="text-left"
            height="250px"
            :src="festival.img"
            cover
            @error="handleImageError(festival.id)"
        >
            <HomeFavouriteBy :festival="festival" />
        </v-img>
        <v-sheet
            v-else
            color="secondary"
            class="text-left"
            variant="text"
        >
            <HomeFavouriteBy :festival="festival" />
        </v-sheet>
        <v-divider></v-divider>

        <v-card-title class="font-weight-bold">
        {{ festival.name }}
        </v-card-title>

        <HomeLocationName :festival="festival" />

        <v-icon icon="mdi-calendar"></v-icon>
        <v-card-subtitle>
        {{ dateFormat(festival.date_start) }} - {{ dateFormat(festival.date_end) }}
        </v-card-subtitle>

        <!-- so its easier to open each card info -->
        <HomeShowInfo :festivalId="festival.id" :festivalInfo="festival.info" />
        <v-divider></v-divider>
    </v-card>
</template>

<script setup>
    const props = defineProps({
        festivals: Object
    })

    const handleImageError = (id) => {
        props.festivals.filter(festival => festival.id === id)[0].img = 'error'
    }

    const dateFormat = (dateString) => {
        const date = new Date(dateString)
        const locale = navigator.language || 'en-US'

        return new Intl.DateTimeFormat(locale).format(date)
    }
</script>