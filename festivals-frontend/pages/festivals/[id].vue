<template>
    <h2>This is details page for festival with id {{ id }}</h2>
    <button>Add to favorites</button>
    <button>Go to festival forum</button>
    <button @click="edit" v-if="isMod">Edit</button>
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
import authentication from '~/composables/auth'
import * as requests from '../../services/requests'

definePageMeta({
    middleware: 'logedin'
})
    const { access } = authentication()
    const { id } = useRoute().params
    const festival = ref('')
    const currentUser = ref('')
    const isMod = ref(false)

    onMounted(async () => {
        // get festival by id
        const response1 = await requests.getFestivalById(id)
        festival.value = await response1.json()        

        // get current user
        const response2 = await requests.getCurrentUser()
        currentUser.value = await response2.json()

        // check if current user id is in festival mods
        // -> if yes, show edit button
        if (festival.value.mods.includes(currentUser.value.id)) {
            isMod.value = true
        }
    })

    // for now just new request
    const edit = () => {
        useRouter().push({
            name: 'festivals-add-edit-festival-id',
        })
    }
</script>