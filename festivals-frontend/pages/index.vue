<template>
    <!-- sloted menu -->
    <v-container fluid>
        <v-sheet class="pa-4 mx-auto" max-width="800" rounded="lg" width="100%">
            <v-card class="mx-auto px-8 py-8 text-center">
                <v-sheet max-width="400" class="mx-auto mx-8 my-4">
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

                    <!-- filters -->
                    <!-- maybe nearby search -->
                    <v-select
                        v-model="selectedFilter"
                        class="mt-4"
                        label="Filter"
                        :items="['All', 'Best', 'Favorites', 'Local']"
                        variant="outlined"
                        density="compact"
                        rounded
                        max-width="150"
                        @update:modelValue="filterResults"
                    ></v-select>
                </v-sheet>

                <v-divider></v-divider>

                <!-- show results if found -->
                <v-card v-if="results.length" v-for="sFestival in results" :key="sFestival.id" nuxt
                    :to="`/festivals/${sFestival.id}`" hover max-width="400" class="mx-auto mx-8 my-4 text-left"
                    :title="`${sFestival.name}`" :subtitle="`${sFestival.info}`">
                </v-card>
                <!-- show all if not searching or query less than 3 chars -->
                <v-card v-else-if="query.length < 3" v-for="festival in festivals" :key="festival.id" nuxt :to="`/festivals/${festival.id}`" hover
                    max-width="400" class="mx-auto mx-8 my-4 text-left" :title="`${festival.name}`"
                    :subtitle="`${festival.info}`">
                </v-card>
                <!-- show no results found if nothing is found -->
                <v-sheet v-else>No results found</v-sheet>                
            </v-card>
        </v-sheet>
    </v-container>
</template>

<script setup>
    import * as requests from '../services/requests'

    const festivals = ref(null)
    const query = ref('')
    const selectedFilter = ref('All')
    const results = ref([])

    onMounted(async () => {
        const response = await requests.getFestivals()

        if (response.status === 200) {
            festivals.value = await response.json()
        }
    })

    const search = async () => {
      if (query.value.length > 2) { // Start searching after 3 characters
        try {
          const response = await requests.getFestivals(`?search=${query.value}`)
          results.value = await response.json()

        } catch (error) {
          console.error(error)
        }
      } else {
        results.value = []
      }
    }

    const filterResults = async () => {
        console.log(123)
    }
</script>