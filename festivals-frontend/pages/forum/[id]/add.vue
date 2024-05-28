<template>
    <div>Add</div>
    <PostForm :post="post" />
    <button @click="add">Add post</button>
</template>

<script setup>
    import * as requests from '../services/requests'

    const id = ref(null)

    const post = ref({
        title: '',
        text: '',
        label: '',
    })

    onMounted(() => {
        id.value = useRoute().params.id
    })
    
    const add = async() => {
        // only add for now
        const response = await requests.addPost(id.value, post.value)
        const responseData = await response.json()
        post.value = responseData
        
        
        // handle if ok
        console.log(responseData)
        
        // if ok reroute (where????)
        useRouter().push({
            name: 'forum-id-post-pid',
            params: { pid: post.value.id }
        })
    }
</script>