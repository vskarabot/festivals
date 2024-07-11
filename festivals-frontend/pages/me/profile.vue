<template>
    <v-sheet class="pa-4 mx-auto" max-width="600">
        <v-card class="mx-auto px-8 py-8">
            {{ userData }}
            <v-row>
                <v-col class="text-center"><v-avatar>slika</v-avatar></v-col>
            </v-row>
        </v-card>
    </v-sheet>
</template>

<script setup>
    import { onMounted } from 'vue';
    import * as services from '../../services/requests'

    const userData = ref('')

    onMounted(async () => {
        const response = await services.getCurrentUser()
        userData.value = await response.json()
    })
</script>