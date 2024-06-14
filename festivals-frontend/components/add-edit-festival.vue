<template>
    <div>Here we'll add festivals and edit</div>
    <hr>
    <div>
        <form>
            <input type="text" placeholder="Festival name" v-model="festival.name"></input><br>
            <textarea placeholder="Info" v-model="festival.info"></textarea><br>
            <input type="text" placeholder="Website" v-model="festival.website"></input><br>
            <input type="number" step="0.01" placeholder="Latitude" v-model="festival.lat"></input><br>
            <input type="number" step="0.01" placeholder="Longitude" v-model="festival.lon"></input><br>
        </form>
    </div>
    
    <Location v-if="id" :lat="festival.lat" :lon="festival.lon" :geolocationEnabled="true" @location-changed="handleLocationChanged"/>
    <Location v-else :lat="festival.lat" :lon="festival.lon" :geolocationEnabled="true" @location-changed="handleLocationChanged"/>

    <button @click="addOrEdit">{{ buttonText }}</button>
</template>

<script setup>
    import * as requests from '../services/requests'

    const id = ref(null)
    const buttonText = ref('')

    const festival = ref({
        name: '',
        info: '',
        website: '',
        // default is Ljubljana, in future change to location of a user
        lat: 14.5057515,
        lon: 46.0569465
    })
    
    onMounted(async () => {
        id.value = useRoute().params.id

        if (id.value) {
            buttonText.value = 'Edit festival'

            // fetch data to edit specific festival
            const response = await requests.getFestivalById(id.value)
            festival.value = await response.json()
        }
        else {
            buttonText.value = 'Add festival'
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

    const addFestival = async () => {
        const response = await requests.createFestival({
            name: festival.value.name,
            info: festival.value.info,
            website: festival.value.website,
            lat: festival.value.lat,
            lon: festival.value.lon
        })
        
        // handle if fail
        console.log(response.status)

        /* SWITCH TO REPLACE so that we don't have to go back to the list */
        if (response.status === 201)
            useRouter().replace(`/`)
    }

    const editFestival = async() => {
        const response = await requests.updateFestival(id.value, {
            name: festival.value.name,
            info: festival.value.info,
            website: festival.value.website,
            lat: festival.value.lat,
            lon: festival.value.lon
        })

        console.log(response.status)

        useRouter().replace(`/festivals/${id.value}`)
        .then(() => {
            reloadNuxtApp()
        })
    }

    const handleLocationChanged = (location, properties) => {
        festival.value.lat = location[0]
        festival.value.lon = location[1]

        // properties.text & properties.address -> TODO shrani v bazo naslov
        console.log(properties)
    }
</script>