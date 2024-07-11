<template>
    <v-dialog
      v-model="dialog"
      max-width="600"
    >
      <template v-slot:activator="{ props: activatorProps }">
        <v-btn
          prepend-icon="mdi-bed"
          color="primary"
          text="Places to stay"
          variant="tonal"
          v-bind="activatorProps"
        ></v-btn>
      </template>

      <v-card
        prepend-icon="mdi-bed"
        title="Accomodations"
      >
        <v-card-text>
          <v-row dense>
            <v-col
              cols="12"
              sm="6"
            >
                <v-text-field
                    v-model="hotelReactiveOptions.adults"
                    prepend-icon="mdi-account-group"
                    maxlength="1" 
                    type="number" 
                    label="Number of people" 
                    variant="outlined"
                    min="1"
                    max="10"
                />
            </v-col>

            <v-col
              cols="12"
              sm="6"
            >
                <v-text-field
                    v-model="hotelReactiveOptions.rooms"
                    prepend-icon="mdi-door"
                    maxlength="1" 
                    type="number" 
                    label="Number of rooms" 
                    variant="outlined"
                    min="1"
                    max="4"
                />
            </v-col>

            <v-col
              cols="12"
              sm="6"
            >
              <v-text-field
                v-model="hotelReactiveOptions.checkin"
                prepend-icon="mdi-check"
                label="Checkin date"
                type="date"
                variant="outlined"
                required
              ></v-text-field>
            </v-col>

            <v-col
              cols="12"
              sm="6"
            >
              <v-text-field
                v-model="hotelReactiveOptions.checkout"
                prepend-icon="mdi-check-all"
                label="Checkout date"
                type="date"
                variant="outlined"
                required
              ></v-text-field>
            </v-col>

            <v-col
              cols="12"
              sm="6"
            >
              <v-select
                v-model="hotelReactiveOptions.order"
                :items="orderOptions"
                label="Order by"
                variant="outlined"
                required
                prepend-icon="mdi-sort"
                item-title="text"
                item-value="value"
              ></v-select>
            </v-col>

            <v-col
              cols="12"
              sm="6"
            >
              <v-text-field
                v-model="hotelReactiveOptions.maxPricePerNight"
                type="number"
                label="Max price per night"
                min="0"
                step="50"
                variant="outlined"
                hint="Leave empty if no price limitations"
                prepend-icon="mdi-currency-eur"
              />
            </v-col>
          </v-row>

          <p>For more accurate results visit <a href="https://www.booking.com/" target="blank">Booking.com</a></p>

          <!-- Results from booking -->
          <v-sheet v-if="accomodations">
            <v-card v-for="accomodation in accomodations" :key="accomodation.name">
              <v-card-title class="text-h5">
                {{ accomodation.name }}
              </v-card-title>
                <div class="d-flex flex-no-wrap justify-space-between">
                  <div>
                    <v-card-subtitle>{{ accomodation.price }}</v-card-subtitle>
                    <v-card-subtitle>{{ accomodation.location }}</v-card-subtitle>
                    <v-card-subtitle>{{ accomodation.review }}</v-card-subtitle>

                    <v-card-text>This accomodation is {{ accomodation.distance }}'s from the festival.</v-card-text>

                    <v-card-actions>
                      <v-btn
                        class="ms-2"
                        size="small"
                        text="Details"
                        variant="outlined"
                        color="primary"
                        @click="openBookingCom(accomodation.link)"
                      ></v-btn>
                    </v-card-actions>
                  </div>

                  <v-avatar
                    class="ma-3"
                    rounded="0"
                    size="125"
                  >
                    <v-img :src="accomodation.image"></v-img>
                  </v-avatar>
                </div>
              </v-card>
          </v-sheet>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            text="Close"
            variant="plain"
            @click="dialog = false; accomodations = null"
          ></v-btn>

          <v-btn
            color="primary"
            text="Search"
            variant="tonal"
            prepend-icon="mdi-magnify"
            @click="getHotels"
          ></v-btn>
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
            maxPricePerNight: String
        }
    })

    const hotelReactiveOptions = ref({
        lat: props.options.lat,
        lon: props.options.lon,
        adults: props.options.adults,
        rooms: props.options.rooms,
        checkin: props.options.checkin,
        checkout: props.options.checkout,
        maxPricePerNight: props.options.maxPricePerNight,
        order: orderOptions[0].value
    })

    const getHotels = async() => {
        const hotelParams = new URLSearchParams(hotelReactiveOptions.value)
        const data = await fetch(`http://localhost:8000/hotels/?${hotelParams.toString()}`)

        const responseData = await data.json()
        accomodations.value = responseData

    }

    const openBookingCom = (url) => {
        window.open(url, '_blank')
    }
</script>