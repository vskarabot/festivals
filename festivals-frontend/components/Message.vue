<template>
    <div class="my-1">
        <v-row style="width: 100%; overflow-x: hidden;">
            <v-col class="text-center">
                <v-card-subtitle>{{ props.message.time }}</v-card-subtitle>
            </v-col>
            <v-col v-if="props.message.is_author" cols="12" class="d-flex justify-end">
                <v-card flat color="primary" class="rounded-xl">
                    <v-card-text class="py-2">{{ props.message.text }}</v-card-text>
                </v-card>
            </v-col>
            <v-col v-else cols="12" class="d-flex justify-start">
                <v-card color="#049494" class="rounded-xl">
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
</script>