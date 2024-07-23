<template>
    <!-- sloted menu -->
     <v-sheet color="primary">
        <!--<v-container fluid class="px-0 py-0">-->
            <v-sheet class="mx-auto" max-width="700" style="border-radius: 0;" width="100%">
                <v-card class="mx-auto text-center" style="border-radius: 0;" color="primary">
                    <v-card max-width="600" class="mx-auto ma-4 pa-4" color="primary" variant="flat">
                        <v-row class="d-flex align-center">
                            <v-col cols="10" class="text-left px-0">
                                <v-card-text>Want to join us? Create new festival and help others!</v-card-text>
                            </v-col>
                            <v-col cols="2">
                                <v-btn color="teal-lighten-1" icon="mdi-plus" to="/festivals/add-edit-festival"></v-btn>
                            </v-col>
                        </v-row>
                        <v-divider thickness="2"></v-divider>
                        <v-card-title class="text-h4 text-left px-0">Festivals </v-card-title>
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
                            color="teal-lighten-1"
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
                            color="teal-lighten-1"
                            @update:modelValue="getOnlySelectedData"
                        ></v-select>

                        <v-row>
                            <v-col>
                                <v-switch v-model="upcoming" color="teal-lighten-1" label="Show only upcoming" @change="getOnlySelectedData"></v-switch>
                            </v-col>
                            <v-col>
                                <v-switch v-model="favourites" color="teal-lighten-1" label="Show my favorites only" @change="getOnlySelectedData"></v-switch>
                            </v-col>
                        </v-row>

                        <v-divider thickness="2"></v-divider>
                    </v-card>

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
        <!--</v-container>-->
    </v-sheet>
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
            initialLoad.value = false
        } catch (error) {
            console.error(error)
        }
    }

    const getOnlySelectedData = async() => {
        loading.value = true
        const params = makeParams()
        const response = await requests.getFestivals(params)
        results.value = await response.json()
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