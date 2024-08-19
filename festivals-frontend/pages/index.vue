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
                        <v-divider thickness="3"></v-divider>
                        <v-card-title class="text-h4 text-left px-0">Festivals </v-card-title>
                        
                        <v-row>
                            <v-col>
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
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="12" sm="6">
                                <v-text-field v-model="startDate" type="date" variant="outlined" hide-details label="Start date" density="compact" rounded color="teall1" clearable @change="getOnlySelectedData" @click:clear="getOnlySelectedData"></v-text-field>
                            </v-col>
                            <v-col cols="12" sm="6">
                                <v-text-field v-model="endDate" type="date" variant="outlined" hide-details label="End date" density="compact" rounded color="teall1" clearable @change="getOnlySelectedData" @click:clear="getOnlySelectedData"></v-text-field>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="12" sm="6">
                                <v-select
                                    v-model="selectedSort"
                                    label="Sort by"
                                    :items="['Date', 'Popularity']"
                                    variant="outlined"
                                    density="compact"
                                    rounded
                                    hide-details
                                    color="teal-lighten-1"
                                    @update:modelValue="getOnlySelectedData"
                                ></v-select>
                            </v-col>
                            <v-col cols="12" sm="6">
                                <v-select
                                    v-model="selectedFilter"
                                    label="Filter"
                                    :items="filterItems"                                    
                                    variant="outlined"
                                    density="compact"
                                    rounded
                                    hide-details
                                    color="teal-lighten-1"
                                    @update:modelValue="getOnlySelectedData"
                                ></v-select>
                            </v-col>
                        </v-row>
                        <v-divider thickness="3" class="mt-4"></v-divider>
                    </v-card>
                    <!-- show results if found -->
                    <v-progress-circular v-if="loading" indeterminate class="my-2" color="primary"></v-progress-circular>  
                    <HomeHPFestivalCard
                        v-if="festivals.length"
                        :festivals="festivals" 
                    />        
                                
                </v-card>
            </v-sheet>
        <!--</v-container>-->
    </v-sheet>
</template>

<script setup>
    import * as requests from '../services/requests'

    const festivals = ref([])

    const query = ref('')
    const selectedSort = ref('Date')
    const filterItems = ref(
        [
            { title: 'All', value: 'all'},
            { title: 'My favourites', value: 'favourites'},
        ]
    )
    const selectedFilter = ref({ title: 'All', value: 'all'})

    const startDate = ref('')
    const endDate = ref('')

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
            festivals.value = await response.json()
            loading.value = false
        } catch (error) {
            console.error(error)
        }
    }

    const getOnlySelectedData = async() => {
        loading.value = true
        const params = makeParams()
        const response = await requests.getFestivals(params)
        festivals.value = await response.json()
        loading.value = false
    }

    const makeParams = () => {
        let params = "?"
        // leave if here because if other action than search is it would trigger search even if string less than 3
        if (query.value.length > 2)
            params = params + `search=${query.value}&`
        params = params + `sort=${selectedSort.value}&`
        if (selectedFilter.value !== 'all')
            params = params + `favourites=True&`
        if (startDate.value)
            params = params + `start_date=${startDate.value}&`
        if (endDate.value)
            params = params + `end_date=${endDate.value}&`

        return params
    }
</script>