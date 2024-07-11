<template>
    <v-card-actions>
        <v-btn color="primary" variant="plain" text="Explore" :to="`/festivals/${festivalId}`"></v-btn>

        <v-spacer></v-spacer>

        <v-btn v-if="festivalInfo" :icon="show ? 'mdi-chevron-up' : 'mdi-chevron-down'" @click="show = !show"></v-btn>
    </v-card-actions>

    <v-expand-transition>
        <div v-show="show">
            <v-divider></v-divider>

            <v-card-text>
                {{ festivalInfo }}
            </v-card-text>
        </div>
    </v-expand-transition>
</template>

<script setup>
    const props = defineProps({
        festivalId: Number,
        festivalInfo: String
    })

    const show = ref(false)
</script>