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
    <span>First map is for path. Second for choosing sleeping options nearby with parameters.</span>
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

    // pogrunti kako passat na edit podatke -> cene pac se en request (kar je mogoce celo bolse ker vec uporabniku lahko updejta podatke d se ne spremenijo umes??)
    // jutri uzemi si cajt in nrdi use funkcije u posebi fileu in pogrunti ku ta component nrdit
    // d se ne ponavlja koda

    const edit = () => {
        useRouter().push({
            name: 'festivals-add-edit-festival-id',
        })
    }
</script>