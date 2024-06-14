<template>
    <div id="map" style="width: 700px; height: 450px;"></div>
</template>

<script setup>
import mapboxgl from 'mapbox-gl'
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder'

    // styling of map
    useHead({
        link: [
            { rel: 'stylesheet', href: 'https://api.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.css'},
            { rel: "stylesheet", href: "https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v5.0.0/mapbox-gl-geocoder.css"}
        ]
    })

    const props = defineProps({
        lat: Number,
        lon: Number,
        geolocationEnabled: Boolean
    })

    const emit = defineEmits(['location-changed'])

    // mapbox constants
    const MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoidnM3MDE1IiwiYSI6ImNsdmF4OXkxMDAzZmYyam52bHMzMXkzM2YifQ.COvY-tigswKIlF3DRqURfA'
    const MAP_LOOK = 'mapbox://styles/mapbox/outdoors-v12'
    const INITIAL_ZOOM = 16
    const MARKER_COLOR = 'red'
        
    onMounted(() => {        
        // wait for props to load before map is created with watchEffect
        watchEffect(() => {
            if (props.lat && props.lon) {
                // check if in limits
                if (props.lat >= -90 && props.lat <= 90 && props.lon >= -180 && props.lon <= 180) {
                    initializeMap(props.lat, props.lon, props.geolocationEnabled)
                }
            }
        })
    })

    // map, marker has [lon, lat]
    // for some reaason geocoder uses [lat, lon]
    const initializeMap = (lat, lon, geolocationEnabled) => {
        mapboxgl.accessToken = MAPBOX_ACCESS_TOKEN

        const map = new mapboxgl.Map({
            container: 'map',
            style: MAP_LOOK,
            center: [lon, lat],
            zoom: INITIAL_ZOOM
        })

        const marker = new mapboxgl.Marker({ color: MARKER_COLOR })
            .setLngLat([lon, lat])
            .setPopup(new mapboxgl.Popup().setHTML(`<p><b>Festival location</b></p>`))
            .addTo(map)

        
        // if add or edit add geolocation
        if (geolocationEnabled) {
            const geocoder = new MapboxGeocoder({
                accessToken: MAPBOX_ACCESS_TOKEN,
                mapboxgl: mapboxgl
            })
            map.addControl(geocoder)

            geocoder.on('result', (e) => {
                marker.setLngLat(e.result.center.reverse())
                // notify parent component about location change
                emit('location-changed', e.result.center, e.result)
            })
        }
    }

</script>