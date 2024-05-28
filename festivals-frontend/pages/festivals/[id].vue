<template>
    <h2>This is details page for festival with id {{ id }}</h2>

    <button @click="handleFavourite">{{ computeFavouriteText }}</button>

    <NuxtLink :to="`/forum/${id}`">Go to festival forum</NuxtLink>

    <button @click="edit" v-if="festival.is_mod">Edit</button>
    <p>{{ festival }}</p>
    <h2>{{ festival.name }}</h2>
    <p>Info: {{ festival.info }}</p>
    <p>Website: <a :href="festival.website">{{ festival.website }}</a></p>
    <p>Latitude: {{ festival.lat }}</p>
    <p>Longitude: {{ festival.lon }}</p>
    <hr>
    <div>
        <p>Location (for now only location):</p>
        <p>(TODO: On the same map implement bookings with different parameters.)</p>
        <Location :lat="festival.lat" :lon="festival.lon" :geolocationEnabled="false" />
    </div>
</template>

<script setup>
    import * as requests from '../../services/requests'

    const { id } = useRoute().params
    const festival = ref('')
    const currentUser = ref('')

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
</script>