<template>
    <div v-if="posts">
        <div v-for="(post, index) in posts">
            <Post
                :key="post.id"
                :index="index"
                :post="post"
                @like="reaction('like', post.id, index)"
                @dislike="reaction('dislike', post.id, index)"
                @delete="deletePost" 
            />
            <button @click="comments(post)">Comments</button>
        </div>
    </div>
    <div v-else><h2>Loading...</h2></div>
</template>

<script setup>
    import { ref, onMounted } from 'vue'
    import * as requests from '../services/requests'
    
    const festivalId = useRoute().params.id
    const posts = ref([])

    const fetchPosts = async() => {
        const response = await requests.getPosts(festivalId)
        const responseData = await response.json()
        posts.value = responseData
    }

    onMounted(() => {
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

    const comments = (post) => {
        useRouter().push({
            name: 'forum-id-posts-pid',
            params: { id: post.festival, pid: post.id }
        })
    }
    
</script>