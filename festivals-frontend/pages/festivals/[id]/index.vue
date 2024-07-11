<template>
    <v-container fluid>
        <v-sheet class="pa-4 mx-auto" max-width="800" rounded="lg" width="100%">
            <v-card class="mx-auto px-8 py-8">
                <v-img
                    v-if="festival.img"
                    height="300px"
                    :src="festival.img"
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
                <v-btn 
                    v-else-if="festival.is_mod"
                    icon="mdi-pencil" 
                    @click="edit"
                    density="comfortable"
                    class="mx-2 my-2"
                />
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
                <v-divider></v-divider>
                <v-row class="my-4" justify="center">
                    <v-col cols="12" sm="4">
                        <v-card variant="text" class="text-center">
                            <v-icon icon="mdi-map-marker" />
                            <v-card-text v-if="locationName">{{ locationName }}</v-card-text> 
                        </v-card>
                    </v-col>
                    
                    <v-col cols="12" sm="4">
                        <v-card variant="text" class="text-center ">
                            <v-icon icon="mdi-calendar" />
                            <v-card-text v-if="festival.date_start">{{ festival.date_start }} - {{ festival.date_end }}</v-card-text>
                            <v-card-text v-else>No dates yet</v-card-text>
                        </v-card>
                    </v-col>
                    
                    <v-col cols="12" sm="4">
                        <v-card variant="text" class="text-center" color="primary" :href="festival.website" target="_blank">
                            <v-icon icon="mdi-web" />
                            <v-card-text v-if="festival.website">{{ festival.website }}</v-card-text>
                            <v-card-text v-else>No website</v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
                <v-expansion-panels>
                    <v-expansion-panel>
                        <v-expansion-panel-title class="font-weight-bold">
                            About festival
                        </v-expansion-panel-title>
                        <v-expansion-panel-text>
                            {{ festival.info }}
                        </v-expansion-panel-text>
                    </v-expansion-panel>
                    <v-expansion-panel>
                        <v-expansion-panel-title class="font-weight-bold">
                            Sleeping options and directions
                        </v-expansion-panel-title>
                        <v-expansion-panel-text>
                            <v-row>
                                <v-col cols="12" sm="4">
                                    <HotelOptions :options="hotelOptions" />
                                </v-col>
                                <v-col cols="12" sm="8">
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

    const runtimeConfig = useRuntimeConfig()

    const { id } = useRoute().params
    const festival = ref('')
    const locationName = ref('')

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

        const mbLoc = await $fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${festival.value.lon},${festival.value.lat}.json?access_token=${runtimeConfig.public.mapboxToken}`)
        locationName.value = mbLoc.features?.[0]?.place_name
        console.log(locationName)

        // hotel options
        hotelOptions.value.lat = festival.value.lat.toFixed(6)
        hotelOptions.value.lon = festival.value.lon.toFixed(6)
        hotelOptions.value.checkin = '2024-07-07'
        hotelOptions.value.checkout = '2024-07-09'
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