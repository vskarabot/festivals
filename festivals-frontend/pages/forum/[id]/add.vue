<template>
    <v-sheet color="primary">
        <PostForm :post="post" />
        <v-card width="600" color="secondary" class="mx-auto pb-4 text-center" rounded="0">
            <v-btn class="mr-2" color="warning" @click="cancel">
                Cancel
            </v-btn>
            <v-btn color="teal-lighten-1" @click="add">
                Add
            </v-btn>
        </v-card>
    </v-sheet>
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

    const cancel = () => {
        useRouter().back()
    }
</script>