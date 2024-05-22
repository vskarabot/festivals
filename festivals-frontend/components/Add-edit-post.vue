<template>
    <div>Add / edit post</div>
    <div>
        <form>
            <input type="text" placeholder="Title" v-model="post.title"></input><br>
            <textarea placeholder="Text" v-model="post.text"></textarea><br>
            <select v-model="post.label">
                <option value="travel">Travel</option>
                <option value="lineup">Lineup</option>
                <option value="tips">Tips</option>
                <option value="shitpost">Shitpost</option>
            </select><br>
        </form>
    </div>
    
    <button @click="addOrEdit">{{ buttonText }}</button>
</template>

<script setup>
    import * as requests from '../services/requests'

    const id = ref(null)

    const post = ref({
        title: '',
        text: '',
        label: '',
    })

    const props = defineProps ({
        post: Object
    })

    onMounted(() => {
        id.value = useRoute().params.id
        if (props.post) {
            post.value.title = props.post.title
            post.value.text = props.post.text
            post.value.label = props.post.label
        }
    })
    
    const addOrEdit = async() => {
        if (props.post) {
            const response = await requests.editPost(id.value, props.post.id, post.value)
            const responseData = await response.json()
            post.value = responseData
            console.log(responseData)
            
        } else {
            const response = await requests.addPost(id.value, post.value)
            const responseData = await response.json()
            post.value = responseData
            console.log(responseData)
        }

        // if ok reroute (where????)
        useRouter().replace({
            name: 'forum-id-posts-pid',
            params: { pid: post.value.id }
        })
        
    }

    const buttonText = computed(() => {
        return props.post ? 'Edit post' : 'Add post'
    })

</script>