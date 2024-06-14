<template>
    <h2>This is details page for festival with id {{ id }}</h2>

    <button @click="handleFavourite">{{ computeFavouriteText }}</button>

    <NuxtLink :to="`/forum/${id}`">Go to festival forum</NuxtLink>

    <NuxtLink :to="`/festivals/${id}/chats`">Chat</NuxtLink>

    <!-- add link to chat -->

    <button @click="edit" v-if="festival.is_mod">Edit</button>
    <p>{{ festival }}</p>
    <h2>{{ festival.name }}</h2>
    <p>Info: {{ festival.info }}</p>
    <p>Date: </p>
    <p>Website: <a :href="festival.website">{{ festival.website }}</a></p>
    <p>Latitude: {{ festival.lat }}</p>
    <p>Longitude: {{ festival.lon }}</p>

    <p>Nearby accomodations: <button @click="getHotels">Scrap</button></p>

    <div>
        <p>Location: </p>
        <Location :lat="festival.lat" :lon="festival.lon" :geolocationEnabled="false" />
    </div>

    <Hotels v-if="accomodations" :hotels="accomodations" />
</template>

<script setup>
    import * as requests from '../../services/requests'

    const { id } = useRoute().params
    const festival = ref('')
    const currentUser = ref('')
    const accomodations = ref({})

    onMounted(async () => {
        // get festival by id
        const response1 = await requests.getFestivalById(id)
        festival.value = await response1.json()        

        // get current user
        const response2 = await requests.getCurrentUser()
        currentUser.value = await response2.json()
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
        return festival.value.is_favourite ? 'Favourite' : 'Add to favourites'
    })


    const hotelParams = new URLSearchParams({
        place: 'Ljubljana',
        checkin: '2024-7-7',
        checkout: '2024-7-9',
        adults: '2',
        rooms: '1',
        // TODO optionally price min, max are also sent (in backend implemented)
        // TODO ordering 
        // check which paramteres could be also used
        // maybe even currency
    })

    const getHotels = async() => {
        const data = await fetch(`http://localhost:8000/hotels/?${hotelParams.toString()}`)
    
        const responseData = await data.json()
        console.log(responseData)
        //accomodations.value = responseData
    }
</script>