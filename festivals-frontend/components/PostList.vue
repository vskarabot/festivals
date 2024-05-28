<template>
    <div v-if="posts">
        <button @click="addPost" v-if="festivalId">Add post</button>
        <div v-for="(post, index) in posts">
            <PostDetail
                :key="post.id"
                :index="index"
                :post="post"
                @like="reaction('like', post.id, index)"
                @dislike="reaction('dislike', post.id, index)"
                @delete="deletePost"
            />
        </div>
    </div>
    <div v-else><h2>Loading...</h2></div>
</template>

<script setup>
    import { ref } from 'vue'
    import * as requests from '../services/requests'
    import { useRoute } from 'vue-router'

   
    const festivalId = useRoute().params.id
    const posts = ref([])

    const fetchPosts = async() => {
        const response = await requests.getPosts(festivalId)
        const responseData = await response.json()
        posts.value = responseData
    }

    onActivated(() => {
        fetchPosts()
    })

    const reaction = async(action, id, index) => {
        const response = await requests.likePost(id, action)
        
        if (response.status === 200) {
            const responseData = await response.json()
            posts.value[index] = responseData
        }
    }

    const deletePost = async(id, index) => {
        const response = await requests.deletePost(id)

        if (response.status === 204) {
            posts.value.splice(index, 1)
        }
        else {
            console.log("Error while deleting - frontend output")
        }
    }

    const addPost = () => {
        useRouter().push({
            name: 'forum-id-add',
            params: { id: festivalId }
        })
    }
</script>