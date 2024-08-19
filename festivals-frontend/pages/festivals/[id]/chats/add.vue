<template>
    <v-sheet color="primary">
        <v-card class="mx-auto px-8 pb-4 text-center" max-width="600" color="secondary" rounded="0" variant="flat">
            <v-card-title class="text-h5 text-left my-4 px-0">Add new chat</v-card-title>
            <v-text-field v-model="name" variant="outlined" label="Chat name" rounded density="compact" color="teal-lighten-1"
                prepend-icon="mdi-chat">
            </v-text-field>
            
            <v-btn class="mr-2" color="warning" @click="cancel">
                Cancel
            </v-btn>
            <v-btn color="teal-lighten-1" @click="addOrEdit">
                Add
            </v-btn>
        </v-card>
    </v-sheet>
</template>

<script setup>
    import * as requests from '../../services/requests'

    const name = ref('')

    const addOrEdit = () => {
        const response = requests.addChat(useRoute().params.id, name.value)
        console.log(response)
    }

    const cancel = () => {
        useRouter().back()
    }
</script>