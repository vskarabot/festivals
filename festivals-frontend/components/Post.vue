<template>
    <div v-if="index==-1">Single post commentss</div>
    <h2>{{ post.title }}</h2>
    <h4>{{ post.festival_name }}</h4>
    <button @click="emitEvent('like')">Like</button>
    {{ post.number_of_likes }}
    <button @click="emitEvent('dislike')">Dislike</button>
    {{ post.number_of_dislikes }} |||
    {{ post.festival }}
    {{ post.label }}
    {{ post.text }}
    {{ post.time }}

    {{ post.username }}
    
    
    <button @click="edit" v-if="post.is_author">Edit</button>
    <button @click="emitEvent('delete')" v-if="post.is_author || post.can_delete">Delete</button>
</template>

<script setup>
import { ref } from 'vue'

    const props = defineProps({
        post: Object,
        index: Number
    })

    const emit = defineEmits(['like', 'dislike', 'delete'])

    const emitEvent = (action) => {
        emit(action, props.post.id, props.index)
    }

    const edit = () => {
        useRouter().push({
            name: 'forum-id-posts-pid-edit',
            params: { id: props.post.festival, pid: props.post.id }
        })
    }
</script>