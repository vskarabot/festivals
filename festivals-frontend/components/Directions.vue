<template>
  <v-sheet prepend-icon="mdi-directions" color="secondary">
    <!-- class is for removing padding and margin because it is wraped and has double values -->
    <v-card-text class="px-0 py-0">
      <v-row dense>
        <v-col cols="12">
          <mapbox-search-box :access-token="runtimeConfig.public.mapboxToken" :proximity="[props.lon, props.lat]" class="mapbox-search" />
        </v-col>
      </v-row>
      <v-row dense v-if="props.userLocation.length == 2">
        <v-col cols="12" class="d-flex align-center justify-center">
          or
        </v-col>
      </v-row>
      <v-row dense v-if="props.userLocation.length == 2">
        <v-col cols="12" class="d-flex align-center justify-center">
          <v-btn class="mb-4" color="teall1" variant="flat" @click="getDirectionsForCurrentLocation">Use current location</v-btn>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card v-if="showDirections && stepsArray && stepsArray.length" variant="flat" color="card" class="my-1">
        <v-card-text class="font-weight-bold">Directions:</v-card-text>
        <v-divider thickness="2" color="primary"></v-divider>
        <v-virtual-scroll :height="300" :items="stepsArray">
          <template v-slot:default="step">
            <v-card-text class="py-1">
              <v-icon v-if="step.item[0].type === 'turn' && step.item[0].modifier === 'right'" icon="mdi-arrow-right-top"></v-icon>
              <v-icon v-if="step.item[0].type === 'turn' && step.item[0].modifier === 'left'" icon="mdi-arrow-left-top"></v-icon>
              <v-icon v-if="step.item[0].type === 'continue'" icon="mdi-arrow-up"></v-icon>
              <v-icon v-if="step.item[0].type === 'fork'" icon="mdi-directions-fork"></v-icon>
              <v-icon v-if="step.item[0].type === 'rotary'" icon="mdi-rotate-360"></v-icon>
              <v-icon v-if="step.item[0].type === 'arrive'" icon="mdi-flag-checkered"></v-icon>

              {{ step.item[0].instruction }} 
              ({{ (parseInt(step.item[1]) / 1000).toFixed(2) + " km" }})
              
            </v-card-text>
            <v-divider thickness="2" color="primary"></v-divider>
          </template>
        </v-virtual-scroll>
    </v-card>
    <v-card-actions v-if="stepsArray.length" class="px-0 py-0">
      <v-btn variant="flat" color="teall1" @click="hideDirections">
        {{ showDirections ? 'Hide directions' : 'Show directions' }}
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
        myLocation: Array,
        userLocation: Array
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
          stepsArray.value.push([step.maneuver, step.distance])
        }

        console.log(stepsArray.value)

        // lines for drawing on map
        geoLines.value = response.routes[0].geometry.coordinates
        emit('emit-dirs-time-distance', geoLines.value, duration.value, distance.value)
      }
    }

    const hideDirections = () => {
      showDirections.value = !showDirections.value
      emit('show-directions', showDirections.value)
    }

    const getDirectionsForCurrentLocation = async () => {
      startLocation.lat = props.userLocation[0]
      startLocation.lon = props.userLocation[1]
      getDirections()
    }

    onMounted(() => {
      // if user searches location extract itt
      const searchBox = document.querySelector('mapbox-search-box')
      searchBox.addEventListener('retrieve', (e) => {
        const feature = e.detail
        // again wrong order from search-box so lat is in [1] and lon in [0]
        startLocation.lat = feature.features[0].geometry.coordinates[1]
        startLocation.lon = feature.features[0].geometry.coordinates[0]

        getDirections()
      })
    })

</script>