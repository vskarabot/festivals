<template>
<v-sheet class="pa-4 mx-auto" max-width="500">
    <v-card>
        <v-container>
            <v-row>
                <v-col cols="6">
                    <v-responsive aspect-ratio="1">
                        <v-btn 
                            @click="newChat" 
                            class="w-100 h-100"
                            color="primary"
                            rounded="xl"
                        >
                        <v-row>
                            <v-col>
                                <v-icon class="text-center" icon="mdi-plus-circle-outline"></v-icon>
                                <v-card-title>Add new</v-card-title>
                            </v-col>
                        </v-row>
                        </v-btn>
                    </v-responsive>
                </v-col>
                <v-col cols="6" class="d-flex text-center align-center">
                    <p>Bring people together by sharing your thoughts and planning meetups!</p>
                </v-col>
            </v-row>
            <v-row>
                <v-col v-for="chat in chats" :key="chat.id" cols="6">
                    <v-responsive aspect-ratio="1">
                        <v-btn 
                            @click="openChat(chat)" 
                            class="w-100 h-100"
                            variant="tonal"
                            color="primary"
                        >
                            <span class="text-wrap">{{ chat.name }}</span>
                        </v-btn>
                    </v-responsive>
                </v-col>
            </v-row>
        </v-container>
    </v-card>
</v-sheet>
</template>

<script setup>
    import * as requests from '../../services/requests'

    const festivalId = useRoute().params.id
    const chats = ref('')

    onMounted(async () => {
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

    const openChat = (chat) => {
        useRouter().push({
            path: `/festivals/${festivalId}/chats/${chat.id}`
        })
    }
</script>