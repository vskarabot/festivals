<template>
    <v-sheet id="map" style="height: 450px;"></v-sheet>
    <v-card v-if="props.directions?.geoLines" id="overlay">
        <v-icon icon="mdi-car"></v-icon>
        <b>&nbsp;{{ timeOutput }}</b><br> {{ kiloms }}
    </v-card>
</template>

<script setup>
import mapboxgl from 'mapbox-gl'
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder'

    const runtimeConfig = useRuntimeConfig()

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
        geolocationEnabled: Boolean,
        directions: Object
    })

    const emit = defineEmits(['location-changed'])

    // mapbox constants
    const MAP_LOOK = 'mapbox://styles/mapbox/outdoors-v12'
    const INITIAL_ZOOM = 16

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

    const kiloms = computed(() => {
        return (parseInt(props.directions.distance) / 1000).toFixed(2) + " km"
    })

    const timeOutput = computed(() => {
        if (props.directions.duration) {
            const time = secsToDayHourMinute(props.directions.duration)
            const days = time["days"]
            const hours = time["hours"]
            const minutes = time["minutes"]

            const daysStr = days ? `${days} day${days > 1 ? 's' : ''}` : ''
            const hoursStr = `${hours} hour${hours > 1 ? 's' : ''}`
            const minutesStr = `${minutes} minute${minutes > 1 ? 's' : ''}`

            if (days) {
                return `${daysStr}, ${hoursStr}, ${minutesStr}`
            } 
            else if (hours) {
                return `${hoursStr}, ${minutesStr}`
            }
            else {
                return `${minutesStr}`
            }
        }
    })

    const secsToDayHourMinute = () => {
        let seconds = props.directions.duration
        const days = Math.floor(seconds / (24 * 3600))
        seconds %= 24 * 3600
        const hours = Math.floor(seconds / 3600)
        seconds %= 3600
        const minutes = Math.floor(seconds / 60)
        return {
            days,
            hours,
            minutes
        }        
    }

    // map, marker has [lon, lat]
    // for some reaason geocoder uses [lat, lon]
    const initializeMap = (lat, lon, geolocationEnabled) => {
        mapboxgl.accessToken = runtimeConfig.public.mapboxToken

        const map = new mapboxgl.Map({
            container: 'map',
            style: MAP_LOOK,
            center: [lon, lat],
            zoom: INITIAL_ZOOM
        })

        let el = document.createElement('div')
        el.className = 'marker img1'
        const marker = new mapboxgl.Marker(el)
            .setLngLat([lon, lat])
            .addTo(map)

        // TODO : maybe should check the others but leave for now. to many other things to fix/add
        if (props.directions?.geoLines) {
            // add route lines
            map.on('load', () => {
                map.addSource('route', {
                    'type': 'geojson',
                    'data': {
                        'type': 'Feature',
                        'properties': {},
                        'geometry': {
                            'type': 'LineString',
                            'coordinates': props.directions.geoLines
                        }
                    }
                });
                map.addLayer({
                    'id': 'route',
                    'type': 'line',
                    'source': 'route',
                    'layout': {
                        'line-join': 'round',
                        'line-cap': 'round'
                    },
                    'paint': {
                        'line-color': '#005b96',
                        'line-width': 6,
                        'line-opacity': 0.6
                    }
                });
            });

            new mapboxgl.Marker()
                .setLngLat(props.directions.geoLines[0])
                .addTo(map)

            // center map -> we need fitBounds method
            // takes most south-west and most north-east coordinate and recenters

            // most south-west -> min lon & min lat
            // most north-east -> max lon & max lat
            const lonArray = props.directions.geoLines.map(([lon]) => lon)
            const latArray = props.directions.geoLines.map(([, lat]) => lat)
            
            const minLon = lonArray.reduce((a,b) => Math.min(a,b))
            const maxLon = lonArray.reduce((a,b) => Math.max(a,b))
            const minLat = latArray.reduce((a,b) => Math.min(a,b))
            const maxLat = latArray.reduce((a,b) => Math.max(a,b))

            // substract bit more so it's not completely on border
            const southWest = [minLon, minLat]
            const northEast = [maxLon, maxLat]

            // recentre on map
            map.fitBounds(
                [southWest, northEast]
            )
        }

        
        // if add or edit add geolocation
        if (geolocationEnabled) {
            const geocoder = new MapboxGeocoder({
                accessToken: runtimeConfig.public.mapboxToken,
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

<style>
    #overlay {
        position: absolute;
        top: 10px; /* Adjust as needed */
        left: 10px; /* Adjust as needed */
        background: rgba(255, 255, 255, 0.8); /* Semi-transparent background */
        padding: 10px;
        border-radius: 5px;
        z-index: 1; /* Ensure it appears above the map */
        text-align: center;
    }

    .marker {
        background-size: cover;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        cursor: pointer;
        background-color: white;
    }

    .img1 {
        background-image: url(/assets/music-circle-outline.png);
    }
</style>