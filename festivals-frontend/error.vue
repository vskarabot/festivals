<template>
  <NuxtLoadingIndicator />
  <v-sheet class="pa-4 text-center mx-auto" max-width="600" rounded="lg" width="100%">
    <v-card class="mx-auto px-8 py-8">
      <v-card-text class="text-h1">{{ error.statusCode }}</v-card-text>
      <v-card-text class="text-h4">{{ error.statusMessage }}</v-card-text>
      <NuxtLink to="/"><v-btn color="error">Home</v-btn></NuxtLink>
    </v-card>
  </v-sheet>
</template>

<script setup lang="ts">
    import type { NuxtError } from '#app'

    const props = defineProps({
      error: Object as () => NuxtError
    })
</script>
