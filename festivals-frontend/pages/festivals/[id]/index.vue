<template>
    <v-container fluid>
        <v-sheet class="pa-4 mx-auto" max-width="800" rounded="lg" width="100%">
            <v-card class="mx-auto px-8 py-8">
                <v-img
                    height="200px"
                    src="https://prismic-assets-cdn.tomorrowland.com/ZfHqa0mNsf2sHj7b_1690560124716_060398be-b1c7-4895-b463-c3c2326a00df.jpg_3649_17099475688224241168.jpg?crop=5838%2C2180%2C0%2C735&width=1500&height=560"
                    cover
                >
                    <v-btn 
                        v-if="festival.is_mod" 
                        icon="mdi-pencil" 
                        @click="edit"
                        density="comfortable"
                        class="mx-2 my-2"
                    />
                </v-img>
                <v-sheet class="mx-auto text-center">
                    <v-chip
                        class="my-4"
                        color="teal"
                        @click="handleFavourite"
                    >
                        <v-icon v-if="festival.is_favourite" icon="mdi-check" left class="mr-2"></v-icon>
                        {{ computeFavouriteText }}
                    </v-chip>
                </v-sheet>
                <v-sheet max-width="400" class="mx-auto mx-8 my-2 text-center">
                    <div class="text-h5 font-weight-bold">{{ festival.name }}</div>
                </v-sheet>
                <v-sheet class="mx-auto mx-8 my-4 text-center">
                    <v-btn-group v-model="toggle" divided>
                        <v-btn @click="openForum">Forum</v-btn>
                        <v-btn @click="openChat">Chat</v-btn>
                    </v-btn-group>
                </v-sheet>
                <v-card class="my-4">
                    <v-row class="py-4">
                        <v-col cols="12" sm="4" class="text-center">
                            <v-icon icon="mdi-map-marker" /> 
                            <br>
                            Location
                        </v-col>
                        <v-col cols="12" sm="4" class="text-center">
                            <v-icon icon="mdi-calendar" />
                            <br>
                            Date
                        </v-col>
                        <v-col cols="12" sm="4" class="text-center">
                            <v-icon icon="mdi-web" />
                            <br>
                            {{ festival.website }}
                        </v-col>
                    </v-row>
                </v-card>
                <v-expansion-panels>
                    <v-expansion-panel>
                        <v-expansion-panel-title class="font-weight-bold">
                            About festival (info)
                        </v-expansion-panel-title>
                        <v-expansion-panel-text>
                            {{ festival.info }}
                        </v-expansion-panel-text>
                    </v-expansion-panel>
                    <v-expansion-panel>
                        <v-expansion-panel-title class="font-weight-bold">
                            Sleeping and directions
                        </v-expansion-panel-title>
                        <v-expansion-panel-text>
                            <v-row align="center">
                                <v-col cols="12" class="text-center">
                                    <HotelOptions :options="hotelOptions" />
                                </v-col>
                                <v-col cols="12" class="text-center">
                                    <Directions @emit-dirs-time-distance="handleDirections" @show-directions="showOrHideDirections" :lat="festival.lat" :lon="festival.lon" />
                                </v-col>
                            </v-row>
                        </v-expansion-panel-text>
                    </v-expansion-panel>
                </v-expansion-panels>
                <v-card class="my-4">
                    <Location v-if="showPath" :lat="festival.lat" :lon="festival.lon" :geolocationEnabled="false" :directions="directions" />
                    <Location v-else :lat="festival.lat" :lon="festival.lon" :geolocationEnabled="false"  />
                </v-card>
            </v-card>
        </v-sheet>
    </v-container>
</template>

<script setup>
    import * as requests from '../../services/requests'

    const { id } = useRoute().params
    const festival = ref('')
    const hotelOptions = ref({})

    // false in beginning only so that v-if in Location is easier -> we do have to set value to true in handleDirections because of this
    const showPath = ref(false)
    const directions = ref([])

    const toggle = ref(null)

    // check if exists with USEFETCH (we need credentials)

    onMounted(async () => {
        // get festival by id
        const response1 = await requests.getFestivalById(id)
        festival.value = await response1.json()

        // most of it is unnecesary and can be moved to HotelOptions
        hotelOptions.value.lat = festival.value.lat.toFixed(6)
        hotelOptions.value.lon = festival.value.lon.toFixed(6)
        hotelOptions.value.checkin = '2024-07-07'
        hotelOptions.value.checkout = '2024-07-09'
        // from here on to be specific
        hotelOptions.value.adults = '2'
        hotelOptions.value.rooms = '1'
        hotelOptions.value.maxPricePerNight = '100'
    })

    // for now just new request for sending data in edit
    const edit = () => {
        useRouter().push({
            name: 'festivals-add-edit-festival-id',
        })
    }

    const handleFavourite = async() => {
        const response = await requests.addToFavourites(id)
        festival.value = await response.json()
    }

    const computeFavouriteText = computed(() => {
        return festival.value.is_favourite ? 'Personal favourite' : 'Add to favourites'
    })

    const openForum = () => {
        useRouter().push(`/forum/${id}`)
    }

    const openChat = () => {
        useRouter().push(`/festivals/${id}/chats`)
        // <NuxtLink :to="`/festivals/${id}/chats`">Chat</NuxtLink>
    }

    const handleDirections = (geoLines, duration, distance) => {
        // check comment in showPath declaration
        showPath.value = true
        directions.value.geoLines = geoLines
        directions.value.duration = duration
        directions.value.distance = distance
    }

    const showOrHideDirections = (show) => {
        showPath.value = show
    }
</script>