<template>
    <v-sheet color="primary">
        <v-card class="mx-auto px-8 pb-4 text-center" max-width="600" color="secondary" rounded="0" variant="flat">
            <v-card-title v-if="post.title.length" class="text-h5 text-left my-4 px-0">{{ post.title }}</v-card-title>
            <v-card-title v-else class="text-h5 text-left my-4 px-0">Add new post</v-card-title>
            <v-text-field v-model="post.title" variant="outlined" label="Title" rounded density="compact" color="teal-lighten-1"
                prepend-icon="mdi-chat">
            </v-text-field>
            <v-textarea v-model="post.text" placeholder="Write your thoughts." variant="outlined" prepend-icon="mdi-pen"></v-textarea>
            <v-select v-model="post.label" :items="postTypes" label="Post label" variant="outlined"
            required prepend-icon="mdi-label" item-title="text" item-value="value" color="teal-lighten-1"></v-select>
        </v-card>
    </v-sheet>
</template>

<script setup>
    import {postTypes} from '../constants/postsTypes'
    const props = defineProps(['post'])

</script>