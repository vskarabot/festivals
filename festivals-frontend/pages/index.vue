<template>
    <!-- sloted menu -->
    <v-container fluid class="px-0 py-0">
        <v-sheet class="px-4 mx-auto" max-width="800" rounded="lg" width="100%">
            <v-card class="mx-auto px-8 py-8 text-center">
                <v-card-title class="text-left text-h4">Festivals</v-card-title>
                <v-sheet max-width="500" class="mx-auto mx-8 my-4">
                    Didn't find your festival? Create new community for the festival!
                    <NuxtLink to="/festivals/add-edit-festival">Add a festival</NuxtLink>

                    <v-text-field
                        class="mt-4"    
                        v-model="query" 
                        @input="search" 
                        label="Search festivals" 
                        variant="outlined" 
                        append-inner-icon="mdi-magnify"
                        density="compact"
                        hide-details
                        single-line
                        rounded
                    >
                    </v-text-field>
                    <v-select
                        v-model="selectedSort"
                        class="mt-4"
                        label="Sort by"
                        :items="['Date', 'Popularity']"
                        variant="outlined"
                        density="compact"
                        rounded
                        max-width="150"
                        @update:modelValue="getOnlySelectedData"
                    ></v-select>

                    <v-row>
                        <v-col>
                            <v-switch v-model="upcoming" color="indigo" label="Show only upcoming" @change="getOnlySelectedData"></v-switch>
                        </v-col>
                        <v-col>
                            <v-switch v-model="favourites" color="indigo" label="Show my favorites only" @change="getOnlySelectedData"></v-switch>
                        </v-col>
                    </v-row>
                </v-sheet>

                <v-divider></v-divider>

                <!-- show results if found -->
                <v-progress-circular v-if="loading" indeterminate class="my-2"></v-progress-circular>  
                <HomeHPFestivalCard
                    v-if="initialLoad"
                    :festivals="festivals" 
                />
                <HomeHPFestivalCard
                    v-else-if="results && results.length"
                    :festivals="results"
                />
                <v-sheet v-else>No results found</v-sheet>           
                            
            </v-card>
        </v-sheet>
    </v-container>
</template>

<script setup>
    import * as requests from '../services/requests'

    const festivals = ref(null)
    const results = ref([])

    const query = ref('')
    const selectedSort = ref('Date')
    const upcoming = ref(false)
    const favourites = ref(false)

    const initialLoad = ref(true)
    const loading = ref(false)

    onMounted(async () => {
        loading.value = true
        const response = await requests.getFestivals()

        if (response.status === 200) {
            festivals.value = await response.json()
            loading.value = false
        }
    })

    const search = async () => {
        loading.value = true
        const params = makeParams()
        try {
            const response = await requests.getFestivals(params)
            results.value = await response.json()
            loading.value = false
        } catch (error) {
            console.error(error)
        }
    }

    const getOnlySelectedData = async() => {
        loading.value = true
        const params = makeParams()
        const response = await requests.getFestivals(params)
        results.value = await response.json()
        initialLoad.value = false
        loading.value = false
    }

    const makeParams = () => {
        let params = "?"
        // leave if here because if other action than search is it would trigger search even if string less than 3
        if (query.value.length > 2)
            params = params + `search=${query.value}&`
        params = params + `sort=${selectedSort.value}&`
        if (upcoming.value)
            params = params + `upcoming=True&`
        if (favourites.value)
            params = params + `favourites=True&`

        return params
    }
</script>