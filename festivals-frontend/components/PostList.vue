<template>
    <v-sheet class="mx-auto" max-width="800">
        <v-card class="mx-auto rounded-0" variant="flat">
            <v-card class="mx-auto py-4" max-width="500" flat>
                <v-btn @click="addPost" v-if="festivalId" prepend-icon="mdi-plus" color="primary">Add post</v-btn>
            </v-card>
            <v-sheet v-for="(post, index) in posts">
                <PostDetail :key="post.id" :index="index" :post="post" @like="reaction('like', post.id, index)"
                @dislike="reaction('dislike', post.id, index)" @delete="deletePost" />
            </v-sheet>
        </v-card>
    </v-sheet>

</template>

<script setup>
    import * as requests from '../services/requests'
   
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