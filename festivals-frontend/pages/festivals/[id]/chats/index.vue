<template>
<v-sheet class="pa-4 mx-auto" max-width="500">
    <v-card>
        <v-container>
            <v-row>
                <v-col cols="6">
                    <v-responsive aspect-ratio="1">
                        <v-btn 
                            @click="newChat" 
                            prepend-icon="mdi-plus-circle-outline" 
                            class="w-100 h-100"
                            color="primary"
                        >
                            Add new
                        </v-btn>
                    </v-responsive>
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