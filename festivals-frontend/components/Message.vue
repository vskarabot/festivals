<template>
    <div class="my-1">
        <v-row style="width: 100%; overflow-x: hidden;">
            <v-col v-if="time" class="text-center py-0">
                <v-card-subtitle>{{ props.message.time_string }}</v-card-subtitle>
            </v-col>
            
            <v-col v-if="props.message.is_author" cols="12" class="d-flex justify-end">
                <v-card @click="toggleTime" flat color="primary" class="rounded-xl" max-width="300">
                    <v-card-text class="py-2">{{ props.message.text }}</v-card-text>
                </v-card>
            </v-col>
            <v-col v-else cols="12" class="d-flex justify-start">
                <v-card-subtitle class="pt-2 pr-2">{{ message.username }}</v-card-subtitle>
                <v-card @click="toggleTime" color="deep-purple" class="rounded-xl" max-width="300">
                    <v-card-text class="py-2">{{ props.message.text }}</v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </div>
</template>

<script setup>
    const props = defineProps({
        message: Object
    })

    const time = ref(false)

    const toggleTime = () => {
        time.value = !time.value
    }
</script>