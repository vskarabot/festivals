<template>
    <v-sheet class="mx-auto" max-width="800">
        <v-card class="mx-auto rounded-0" variant="flat">
            <v-card class="mx-auto px-2 py-4" max-width="500" flat>
                <v-text-field
                    v-model="searchString"
                    class="mt-4"    
                    label="Search posts" 
                    variant="outlined" 
                    append-icon="mdi-magnify"
                    density="compact"
                    hide-details
                    single-line
                    rounded
                    @input="fetchPosts"
                >
                </v-text-field>

                <v-row class="mt-2">
                    <v-col cols="6">
                        <v-select
                            v-model="filter"
                            label="Filter"
                            :items="['All', 'Shitpost', 'Lineup', 'Travel', 'Tips']"
                            variant="outlined"
                            density="compact"
                            rounded
                            @update:modelValue="fetchPosts"
                        ></v-select>
                    </v-col>
                    <v-col cols="6">
                        <v-select
                            v-model="sort"
                            label="Sort by"
                            :items="['Best', 'New', 'Top', 'Controversial', 'Most commented']"
                            variant="outlined"
                            density="compact"
                            rounded
                            @update:modelValue="fetchPosts"
                        ></v-select>
                    </v-col>                    
                </v-row>
                <v-btn @click="addPost" v-if="festivalId" rounded="xl" prepend-icon="mdi-plus" color="primary">Add post</v-btn>
            </v-card>
            <v-sheet v-if="showLoading" class="text-center my-2">
                <v-progress-circular indeterminate></v-progress-circular>
            </v-sheet>
            <v-sheet v-for="(post, index) in posts">
                <PostDetail :key="post.id" :index="index" :post="post" @like="reaction('like', post.id, index)"
                @dislike="reaction('dislike', post.id, index)" @delete="deletePost" />
            </v-sheet>
            <v-sheet v-if="!posts.length && !initialLoad" class="text-center my-2">
                <v-card-text>No posts found!</v-card-text>
            </v-sheet>
        </v-card>
    </v-sheet>

</template>

<script setup>
    import * as requests from '../services/requests'
   
    const festivalId = useRoute().params.id
    const posts = ref([])

    const filter = ref('All')
    const sort = ref('New')
    const searchString = ref('')

    const showLoading = ref(false)
    const initialLoad = ref(true)

    const fetchPosts = async() => {
        showLoading.value = true
        const params = makeParams()
        const response = await requests.getPosts(festivalId, params)
        const responseData = await response.json()
        posts.value = responseData
        showLoading.value = false
    }

    onMounted(async() => {
        await fetchPosts()
        initialLoad.value = false
    })
    onActivated(async() => {
        await fetchPosts()
        initialLoad.value = false
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

    const makeParams = () => {
        let params = festivalId ? '' : '?'
        if (searchString.value)
            params += `search=${searchString.value}&`
        if (filter.value)
            params += `filter=${filter.value}&`
        if (sort.value)
            params += `sort=${sort.value}&`

        return params
    }
</script>