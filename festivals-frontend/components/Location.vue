<template>
    <v-sheet id="map" style="height: 450px;"></v-sheet>
    <div v-if="props.directions?.geoLines" id="overlay">
        {{ props.directions.duration }}
        {{ props.directions.distance }}
    </div>
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
        geolocationEnabled: Boolean,
        directions: Object
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
            const southWest = [minLon-0.1, minLat-0.1]
            const northEast = [maxLon+0.1, maxLat+0.1]

            // recentre on map
            map.fitBounds(
                [southWest, northEast]
            )
        }

        
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

<style>
    #overlay {
        position: absolute;
        top: 10px; /* Adjust as needed */
        left: 10px; /* Adjust as needed */
        background: rgba(255, 255, 255, 0.8); /* Semi-transparent background */
        padding: 10px;
        border-radius: 5px;
        z-index: 1; /* Ensure it appears above the map */
    }
</style>