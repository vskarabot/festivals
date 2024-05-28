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
        
        try {
            const state = useState('editPostData')
            post.value.title = state.value.title
            post.value.text = state.value.text
            post.value.label = state.value.label
        // if values not found (refresh or direct access) -> redirect
        } catch (e) {
            useRouter().replace({
                name: 'forum-id-post-pid',
                params: { pid: post.value.id }
            })
        }
    })
    
    const edit = async() => {
        // only add for now
        const response = await requests.editPost(id.value, useRoute().params.pid, post.value)
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