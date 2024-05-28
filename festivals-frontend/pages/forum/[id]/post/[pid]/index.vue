<template>
    <div v-if="post && !post.detail">
        {{ post }}
        <h2>{{ post.title }}</h2>
        <h4>{{ post.festival_name }}</h4>
        <button @click="reaction('like')">Like</button>
        {{ post.number_of_likes }}
        <button @click="reaction('dislike')">Dislike</button>
        {{ post.number_of_dislikes }}
        
        
        <button @click="edit" v-if="post.is_author">Edit</button>
        <button @click="deletePost" v-if="post.is_author || post.can_delete">Delete</button>
        <hr>

        <!-- TODO Missing edit, comments (specific post page) -->
    </div>
    <div v-else><h2>oops</h2></div>
</template>

<script setup>
    // single post (when finished try to join with some other codes)
    import * as requests from '../../../../../services/requests'

    const post = ref(null)

    onActivated(async() => {
        const response = await requests.getPostDetail(useRoute().params.pid)
        const responseData = await response.json()
        post.value = responseData
        console.log(post.value)
    })

    const reaction = async(action) => {
        const response = await requests.likePost(useRoute().params.pid, action)
        
        if (response.status === 200) {
            const responseData = await response.json()
            post.value = responseData
        }
    }

    const deletePost = async() => {
        const response = await requests.deletePost(useRoute().params.pid)
        
        if (response.status === 204) {
            useRouter().replace({
                name: 'forum-id',
                params: { id: post.value.festival }
            })
        }
    }

    const edit = () => {
        useRouter().push({
            name: 'forum-id-post-pid-edit',
            params: { id: post.value.festival, pid: post.value.id }
        })
    }
</script>
