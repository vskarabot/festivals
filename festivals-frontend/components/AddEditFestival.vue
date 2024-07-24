<template>
    <v-sheet color="primary">
        <v-card class="mx-auto px-8 pb-4 text-center" max-width="600" color="secondary" rounded="0" variant="flat">
            <v-card-title class="text-h5 text-left my-4 px-0">{{ buttonValue }}</v-card-title>
            <v-text-field v-model="festival.name" variant="outlined" label="Name" rounded density="compact" color="teal-lighten-1"
                prepend-icon="mdi-music-box">
            </v-text-field>
            <v-textarea v-model="festival.info" variant="outlined" label="Information" rounded density="compact" color="teal-lighten-1"
                prepend-icon="mdi-information">
            </v-textarea>
            <v-text-field v-model="festival.date_start" variant="outlined" type="date" label="Start date" rounded color="teal-lighten-1"
                density="compact" prepend-icon="mdi-calendar-start">
            </v-text-field>
            <v-text-field v-model="festival.date_end" variant="outlined" type="date" label="End date" rounded color="teal-lighten-1"
                density="compact" prepend-icon="mdi-calendar-end">
            </v-text-field>
            <v-text-field v-model="festival.website" variant="outlined" label="Website" rounded density="compact" color="teal-lighten-1"
                prepend-icon="mdi-web">
            </v-text-field>
            <v-file-input v-model="festival.img" variant="outlined" label="Image" rounded density="compact" color="teal-lighten-1"
                prepend-icon="mdi-image">
            </v-file-input>
            <v-text-field v-if="locationName" class="mt-4 text-left" variant="outlined" readonly rounded density="compact" 
                prepend-icon="mdi-map-marker">
                {{ locationName }}
            </v-text-field> 
            <v-text-field v-model="festival.lat" variant="outlined" label="Latitude" rounded density="compact" color="teal-lighten-1"
                prepend-icon="mdi-latitude">
            </v-text-field>
            <v-text-field v-model="festival.lon" variant="outlined" label="Longitude" rounded density="compact" color="teal-lighten-1"
                prepend-icon="mdi-longitude">
            </v-text-field>
            <v-btn class="mr-2" color="warning" @click="cancel">
                Cancel
            </v-btn>
            <v-btn color="teal-lighten-1" @click="addOrEdit">
                {{ buttonValue }}
            </v-btn>
        </v-card>
        <v-card rounded="0">
            <Location :lat="festival.lat" :lon="festival.lon" :geolocationEnabled="true" @location-changed="handleLocationChanged" />
        </v-card>
    </v-sheet>
</template>

<script setup>
    import * as requests from '../services/requests'

    const runtimeConfig = useRuntimeConfig()

    const id = ref(null)
    
    const locationName = ref('')

    const festival = ref({
        name: '',
        info: '',
        website: '',
        // default is Ljubljana, in future change to location of a user
        lat: 46.0569465,
        lon: 14.5057515,
        start_date: '',
        end_date: '',
        img: ''
    })

    const buttonValue = computed(() => {
        return useRoute().params.id ? 'Edit festival' : 'New festival'
    })

    onMounted(async () => {
        id.value = useRoute().params.id

        const mbLoc = await $fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${festival.value.lon},${festival.value.lat}.json?access_token=${runtimeConfig.public.mapboxToken}`)
        locationName.value = mbLoc.features?.[0]?.place_name

        if (id.value) {

            // fetch data to edit specific festival
            const response = await requests.getFestivalById(id.value)
            festival.value = await response.json()
        }
        else {
            
            // set initial dates if adding new
            const dateToday = new Date()
            let dateToday3 = new Date(dateToday)
            dateToday3.setDate(dateToday3.getDate() + 3)            
            festival.value.start_date = dateToday.toISOString().substring(0,10)
            festival.value.end_date = dateToday3.toISOString().substring(0,10)
        }
    })

    const addOrEdit = () => {
        if (id.value) {
            editFestival()
        }
        else {
            addFestival()
        }
    }

    // image uploading
    import { uploadBytes, ref as storageRef, getDownloadURL } from 'firebase/storage'
    const uploadImage = async() => {
        // storage instance from firebase.ts
        const storage = useNuxtApp().$storage
        // reference to location in storage - date to make name unique
        const fileName = `festival-themes/${Date.now()}-${festival.value.img.name}`
        const imageRef = storageRef(storage, fileName)

        try {
            // upload file
            await uploadBytes(imageRef, festival.value.img)
            // get file url
            const url = await getDownloadURL(imageRef)
            return url 
        }
        catch (error) {
            console.log("Error uploading image")
        }
    }

    const addFestival = async () => {
        const addData = {}
        if (festival.value.img) {
            const url = await uploadImage()
            if (url) {
                addData.img = url
            }
        }

        addData.name = festival.value.name
        addData.info = festival.value.info
        addData.website = festival.value.website
        addData.lat = festival.value.lat
        addData.lon = festival.value.lon
        addData.date_start = festival.value.date_start
        addData.date_end = festival.value.date_end

        const response = await requests.createFestival(addData)
        const responseData = await response.json()

        if (response.status === 201)
            useRouter().replace(`/festivals/${responseData.id}`)
    }

    const editFestival = async() => {
        const addData = {}
        if (festival.value.img) {
            const url = await uploadImage()
            if (url) {
                addData.img = url
            }
        }

        addData.name = festival.value.name
        addData.info = festival.value.info
        addData.website = festival.value.website
        addData.lat = festival.value.lat
        addData.lon = festival.value.lon
        addData.date_start = festival.value.date_start
        addData.date_end = festival.value.date_end

        const response = await requests.updateFestival(id.value, addData)
        const responseData = await response.json()

        if (response.status === 200)
            useRouter().replace(`/festivals/${responseData.id}`)
    }

    const handleLocationChanged = (location, properties) => {
        festival.value.lat = location[0]
        festival.value.lon = location[1]
        // properties.text & properties.place_name

        locationName.value = properties.place_name
    }

    const cancel = () => {
        if (id.value) {
            useRouter().replace(`/festivals/${id.value}`)
        }
        else {
            useRouter().replace("/")
        }
    }
</script>