<template>
    <div>Add new chat</div>
    <div>
        <form>
            <input type="text" placeholder="Chat name" v-model="name"></input>
        </form>
    </div>
    <button @click="addOrEdit">Add chat</button>
</template>

<script setup>
    import * as requests from '../../services/requests'

    const name = ref('')

    const addOrEdit = () => {
        const response = requests.addChat(useRoute().params.id, name.value)
        console.log(response)
    }
</script>