<template>
    <div>
      <input v-model="query" @input="search" placeholder="Search for festivals">
      <ul v-if="results.length">
        <li v-for="festival in results" :key="festival.id">{{ festival.name }}</li>
      </ul>
      <p v-else-if="!query.length"></p>
      <p v-else-if="query.length>2">No results found</p>
    </div>
  </template>
  
  <script setup>
  import * as requests from '../services/requests'

  const query = ref('')
  const results = ref([])

  const search = async() => {
    if (query.value.length > 2) { // Start searching after 3 characters
        try {
            const response = await requests.getFestivals(`?search=${query.value}`)          
            results.value = await response.json()
        
        } catch (error) {
            console.error(error)
        }
    } else {
        results.value = []
    }
  }
  </script>
  