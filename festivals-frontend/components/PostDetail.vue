<template>
    {{ post }}
    <h2>{{ post.title }}</h2>
    <h4>{{ post.festival_name }}</h4>
    <button @click="emitEvent('like')">Like</button>
    {{ post.number_of_likes }}
    <button @click="emitEvent('dislike')">Dislike</button>
    {{ post.number_of_dislikes }}
    
    
    <button @click="edit" v-if="post.is_author">Edit</button>
    <button @click="emitEvent('delete')" v-if="post.is_author || post.can_delete">Delete</button>
    <button @click="openPost" >Comments</button>
    <hr>

    <!-- TODO Missing edit, comments (specific post page) -->

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


    const openPost = () => {
        useRouter().push({
            name: 'forum-id-post-pid',
            params: { id: props.post.festival, pid: props.post.id }
        })
    }

    const edit = () => {
        // state of post to edit (for AddEditPost.vue) -> so we dont have to fetch it again
        useState('editPostData', () => props.post)

        useRouter().push({
            name: 'forum-id-post-pid-edit',
            params: { id: props.post.festival, pid: props.post.id }
        })
    }
</script>