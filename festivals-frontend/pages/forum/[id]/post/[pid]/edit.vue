<template>
    <div>Edit</div>
    <PostForm :post="post" />
    <button @click="edit">Edit post</button>
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
    
    const edit = async() => {
        // only add for now
        const response = await requests.editPost(id.value, useRoute().params.pid, post.value)
        const responseData = await response.json()
        post.value = responseData        
        
        // handle if ok
        console.log(responseData)
        
        // if ok reroute (where????)
        useRouter().back()
    }
</script>