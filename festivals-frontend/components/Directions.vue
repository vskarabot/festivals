<template>
    <v-sheet
      prepend-icon="mdi-directions"
      title="Directions"
    >
    <v-divider></v-divider>
      <v-card-text>
        <v-row dense>
          <v-col
            cols="12"
            sm="9"
          >
              <mapbox-search-box
                
                access-token='pk.eyJ1IjoidnM3MDE1IiwiYSI6ImNsdmF4OXkxMDAzZmYyam52bHMzMXkzM2YifQ.COvY-tigswKIlF3DRqURfA'
                proximity="0,0"
              />
          </v-col>
          <v-col
            cols="12"
            sm="3"
            class="text-center"
          >
            <v-btn-toggle v-model="travelOption">
              <v-btn value="driving"><v-icon icon="mdi-car"></v-icon></v-btn>
              <v-btn value="walking"><v-icon icon="mdi-walk"></v-icon></v-btn>
            </v-btn-toggle>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions v-if="stepsArray.length">
        <v-btn color="warning" @click="hideDirections" class="text-left">
          Hide/Show
        </v-btn>
      </v-card-actions>
      <v-sheet v-if="showDirections && stepsArray.length">
        Steps:
        <v-card-text>
          {{ stepsArray }}
        </v-card-text>
      </v-sheet>
    </v-sheet>
</template>

<script setup>
    const travelOption = ref('driving')
    const endLocation = ref('')

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
      const response = await $fetch(`https://api.mapbox.com/directions/v5/mapbox/${travelOption.value}/${props.lon}%2C${props.lat}%3B${endLocation.lon}%2C${endLocation.lat}?alternatives=false&geometries=geojson&language=en&overview=simplified&steps=true&access_token=pk.eyJ1IjoidnM3MDE1IiwiYSI6ImNsdmF4M2tmMzAyaWUyanJzcHc2bjA4emIifQ.s6PCMCZ_MgHzrI5E29wlWg`)
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
        endLocation.lat = feature.features[0].geometry.coordinates[1]
        endLocation.lon = feature.features[0].geometry.coordinates[0]

        getDirections()
      })
    })

    // TODO -> endLocation is wrong now (i set starting location to the festival)
</script>