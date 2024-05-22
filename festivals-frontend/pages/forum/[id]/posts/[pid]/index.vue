<template>
    <Posts />
</template>

<script setup>
    const pid = useRoute().params.pid
    console.log(pid)
</script>