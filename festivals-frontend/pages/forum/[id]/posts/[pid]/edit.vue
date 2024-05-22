<template>
    <!-- for now it only adds so fix to use patch if edit (inside add-edit-post.vue )-->
    <Add-edit-post :post="post" v-if="post" />
</template>

<script setup>
    import * as requests from '../../../../../services/requests'
    const post = ref('')

    const pid = useRoute().params.pid

    onMounted(async () => {
        const response = await requests.getPostDetail(pid)
        const responseData = await response.json()

        post.value = responseData
    })
</script>