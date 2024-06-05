<template>
    chat list for specific festival {{ festivalId }}

    <button @click="newChat">Add new</button>

    <div v-for="chat in chats" :key="chat.id">
        <NuxtLink :to="`/festivals/${festivalId}/chats/${chat.id}`">{{ chat }}</NuxtLink>
    </div>
</template>

<script setup>
    import * as requests from '../../services/requests'

    const festivalId = useRoute().params.id
    const chats = ref('')

    onMounted(async() => {
        // get chats for festival {id}

        const response = await requests.getChats(festivalId)
        const responseData = await response.json()
        chats.value = responseData
    })

    const newChat = () => {
        useRouter().push({
            path: `/festivals/${festivalId}/chats/add`
        })
    }
</script>