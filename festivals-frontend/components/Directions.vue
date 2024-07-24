<template>
  <v-sheet prepend-icon="mdi-directions" color="secondary">
    <!-- class is for removing padding and margin because it is wraped and has double values -->
    <v-card-text class="px-0 py-0">
      <v-row dense>
        <v-col cols="1" class="px-0 py-0 d-flex align-center justify-center">
          <v-icon icon="mdi-car" color="teal-lighten-1"/>
        </v-col>
        <v-col cols="11">
          <mapbox-search-box :access-token="runtimeConfig.public.mapboxToken" proximity="0,0" class="mapbox-search" />
        </v-col>
      </v-row>
    </v-card-text>
    <v-card v-if="showDirections && stepsArray.length" variant="outlined" color="purple-darken-4" class="my-1">
      <v-sheet>
        <v-card-text class="font-weight-bold">Directions:</v-card-text>
        <v-divider></v-divider>
        <v-virtual-scroll :height="300" :items="stepsArray">
          <template v-slot:default="step">
            <v-card-text class="py-1">
              {{ step.index + 1 }}. {{ step.item }}
            </v-card-text>
          </template>
        </v-virtual-scroll>
      </v-sheet>
    </v-card>
    <v-card-actions v-if="stepsArray.length" class="px-0 py-0">
      <v-btn variant="tonal" color="purple-darken-4" @click="hideDirections">
        {{ showDirections ? 'Hide' : 'Show' }}
      </v-btn>
    </v-card-actions>
  </v-sheet>
</template>

<script setup>
    const runtimeConfig = useRuntimeConfig()

    const startLocation = ref('')

    const stepsArray = ref([])
    const distance = ref('')
    const duration = ref('')
    const geoLines = ref('')
    const showDirections = ref(true)

    const props = defineProps({
        lat: String,
        lon: String,
    })

    const emit = defineEmits(['emit-dirs-time-distance', 'show-directions'])

    useHead({
      script: [{
          src: "https://api.mapbox.com/search-js/v1.0.0-beta.21/web.js",
          defer: true,
          id: 'search-js'
      }]
    })

    const getDirections = async() => {
      // longitude, latitude

      // TODO (not really) overview -> simplified ; 
      // if needed we'll change but it is a lot of data to show perfect path
      const response = await $fetch(`https://api.mapbox.com/directions/v5/mapbox/driving/${startLocation.lon}%2C${startLocation.lat}%3B${props.lon}%2C${props.lat}?alternatives=false&geometries=geojson&language=en&overview=simplified&steps=true&access_token=${runtimeConfig.public.mapboxToken}`)
      if (response.code === "Ok") {
        
        distance.value = response.routes[0].distance
        // value is in seconds now
        duration.value = response.routes[0].duration

        const steps = response.routes[0].legs[0].steps
        stepsArray.value = []
        for (let step of steps) {
          stepsArray.value.push(step.maneuver.instruction)
        }

        // lines for drawing on map
        geoLines.value = response.routes[0].geometry.coordinates
        emit('emit-dirs-time-distance', geoLines.value, duration.value, distance.value)
      }
    }

    const hideDirections = () => {
      showDirections.value = !showDirections.value
      emit('show-directions', showDirections.value)
    }

    onMounted(() => {
      const searchBox = document.querySelector('mapbox-search-box')

      searchBox.addEventListener('retrieve', (e) => {
        const feature = e.detail
        // again wrong order from search-box so lat is in [1] and lon in [0]
        startLocation.lat = feature.features[0].geometry.coordinates[1]
        startLocation.lon = feature.features[0].geometry.coordinates[0]

        getDirections()
      })
    })

    // TODO -> endLocation is wrong now (i set starting location to the festival)
</script>

<style scoped>
  .custom-mapbox-search-box .mapboxgl-ctrl-geocoder--input {
    border-color: red; /* Change the border color */
  }
</style>