<template>
    <v-sheet color="primary">
        <PostForm :post="post" />
        <v-card width="600" color="secondary" class="mx-auto pb-4 text-center" rounded="0">
            <v-btn class="mr-2" color="warning" @click="cancel">
                Cancel
            </v-btn>
            <v-btn color="teal-lighten-1" @click="edit">
                Edit
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

    onMounted(async() => {
        id.value = useRoute().params.id
        const res = await requests.getPostDetail(useRoute().params.pid) 
        const resData = await res.json()
        post.value.title = resData.title
        post.value.text = resData.text
        post.value.label = resData.label
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

    const cancel = () => {
        useRouter().back()
    }
</script>