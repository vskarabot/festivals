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
        <v-img
            v-if="festival.img"
            class="text-left"
            height="250px"
            :src="festival.img"
            cover
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

        <v-card-title>
        {{ festival.name }}
        </v-card-title>

        <HomeLocationName :festival="festival" />

        <v-card-subtitle>
        {{ festival.date_start }} {{ festival.date_end }}
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

</script>