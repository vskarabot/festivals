<template>
    <v-chip :color="getColor(props.label)" size="small">
        {{ props.label }}
    </v-chip>
</template>

<script setup>
    const props = defineProps({
        label: String
    })

    const getColor = (label) => {
        if (label === 'shitpost')
            return 'red'
        else if (label === 'travel')
            return 'cyan'
        else if (label === 'lineup')
            return 'success'
        else
            return 'pink'
    }
</script>