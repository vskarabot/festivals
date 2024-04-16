<template>
    <div>Here we'll add festivals</div>
    <hr>
    <div>
        <form>
            <input type="text" placeholder="Festival name" v-model="name"></input><br>
            <textarea placeholder="Info" v-model="info"></textarea><br>
            <input type="text" placeholder="Website" v-model="website"></input><br>
            <input type="number" step="0.01" placeholder="Latitude" v-model="lat"></input><br>
            <input type="number" step="0.01" placeholder="Longitude" v-model="lon"></input><br>
        </form>
    </div>
    <button @click="addFestival">Add festival</button>
</template>

<script>
    export default {
        data() {
            return {
                name: '',
                info: '',
                website: '',
                lat: null,
                lon: null
            }
        },
        methods: {
            async addFestival() {
                const res = await fetch('http://localhost:8000/festivals/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        name: this.name,
                        info: this.info,
                        website: this.website,
                        lat: this.lat,
                        lon: this.lon
                    })
                });

                const data = await res.json()
            }
        }
    }
</script>