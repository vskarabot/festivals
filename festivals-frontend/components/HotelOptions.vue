<template>
  <v-dialog v-model="dialog" max-width="600">
    <template v-slot:activator="{ props: activatorProps }">
      <v-btn prepend-icon="mdi-bed" color="teal-lighten-1" text="Places to stay" variant="flat"
        v-bind="activatorProps"></v-btn>
    </template>

    <v-card prepend-icon="mdi-bed" title="Accomodations" color="primary">
      <v-card-text v-if="props.options.tookPlace" class="text-error">{{ props.options.tookPlace }}</v-card-text>
      <v-card-text class="pt-4">
        <v-row dense>
          <v-col cols="12" sm="6">
            <v-text-field v-model="hotelReactiveOptions.adults" prepend-icon="mdi-account-group" maxlength="1"
              type="number" label="Number of people" variant="outlined" min="1" max="10" color="teal-lighten-1">
            </v-text-field>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field v-model="hotelReactiveOptions.rooms" prepend-icon="mdi-door" maxlength="1" type="number"
              label="Number of rooms" variant="outlined" min="1" max="4" color="teal-lighten-1" />
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field v-model="hotelReactiveOptions.checkin" prepend-icon="mdi-check" label="Checkin date"
              type="date" variant="outlined" required color="teal-lighten-1"></v-text-field>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field v-model="hotelReactiveOptions.checkout" prepend-icon="mdi-check-all" label="Checkout date"
              type="date" variant="outlined" required color="teal-lighten-1"></v-text-field>
          </v-col>

          <v-col cols="12" sm="6">
            <v-select v-model="hotelReactiveOptions.order" :items="orderOptions" label="Order by" variant="outlined"
              required prepend-icon="mdi-sort" item-title="text" item-value="value" color="teal-lighten-1"></v-select>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field v-model="hotelReactiveOptions.maxPricePerNight" type="number" label="Max price per night"
              min="0" step="50" variant="outlined" hint="Leave empty if no price limitations"
              prepend-icon="mdi-currency-eur" color="teal-lighten-1" />
          </v-col>
        </v-row>

        <v-card-text class="pa-0 ma-0">For more accurate results visit <a href="https://booking.com/"
            target="_blank">Booking.com</a></v-card-text>

        <!-- Results from booking -->
        <v-sheet v-if="accomodations" class="my-4">
          <v-card v-for="accomodation in accomodations" :key="accomodation.name" color="secondary" rounded="0">
            <v-card-title class="text-h5">
              {{ accomodation.name }}
            </v-card-title>

            <v-divider></v-divider>

            <v-card color="secondary" variant="flat" class="px-4 py-4">
              <v-row>
                <v-col cols="12" sm="6">
                  <v-chip-group column>
                    <v-chip>
                      <v-card-text class="px-0">{{ accomodation.price }}</v-card-text>
                    </v-chip>
                    <v-chip>
                      <v-icon icon="mdi-map-marker"></v-icon>
                      <v-card-text class="px-0">{{ accomodation.location }}</v-card-text>
                    </v-chip>
                    <v-chip>
                      <v-icon icon="mdi-star"></v-icon>
                      <v-card-text class="pl-2 pr-0">{{ accomodation.review }}</v-card-text>
                    </v-chip>
                  </v-chip-group>
                  <v-card-text class="px-0">This accomodation is {{ accomodation.distance }}'s from the
                    festival.</v-card-text>

                  <v-card-actions class="px-0">
                    <v-btn size="small" text="Details" variant="flat" color="teall1"
                      @click="openBookingCom(accomodation.link)"></v-btn>
                  </v-card-actions>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-img :src="accomodation.image" cover></v-img>
                </v-col>
              </v-row>
            </v-card>
            <v-divider thickness="10" color="primary" opacity="10"></v-divider>

          </v-card>
        </v-sheet>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn text="Close" color="warning" variant="flat" @click="dialog = false; accomodations = null"></v-btn>

        <v-btn color="teall1" text="Search" variant="flat" prepend-icon="mdi-magnify" @click="getHotels"></v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { orderOptions } from '../constants/hotels'

const dialog = ref(false)
const accomodations = ref()

const props = defineProps({
  options: {
    lat: String,
    lon: String,
    adults: String,
    rooms: String,
    checkin: String,
    checkout: String,
    maxPricePerNight: String,
    tookPlace: String
  }
})

const hotelReactiveOptions = ref({})

onMounted(() => {
  hotelReactiveOptions.value = {
    lat: props.options.lat,
    lon: props.options.lon,
    adults: props.options.adults,
    rooms: props.options.rooms,
    checkin: props.options.checkin,
    checkout: props.options.checkout,
    maxPricePerNight: props.options.maxPricePerNight,
    order: orderOptions[0].value
  }
})

const getHotels = async () => {
  const hotelParams = new URLSearchParams(hotelReactiveOptions.value)
  const data = await fetch(`http://localhost:8000/hotels/?${hotelParams.toString()}`)

  const responseData = await data.json()
  accomodations.value = responseData

}

const openBookingCom = (url) => {
  window.open(url, '_blank')
}
</script>

<style scoped>
a {
  text-decoration: none;
  color: #26A69A;
}

a:hover {
  text-decoration: underline;
}
</style>