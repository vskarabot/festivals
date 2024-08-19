<template>
    <div class="my-1">
        <v-row style="width: 100%; overflow-x: hidden;">
            <v-col class="text-center px-0 pt-4 pb-0">
                <v-card-subtitle>{{ props.message.messageShowTimeIntervals }}</v-card-subtitle>
            </v-col>

            <v-col
                cols="12"
                :class="props.message.author == userId ? 'd-flex justify-end':'d-flex justify-start'"
            >
                <v-badge dot v-if="props.message.author != userId" class="d-flex align-center ml-4 mr-2" color="card">
                    <v-chip variant="flat" color="secondary" class="px-2">
                        <v-icon>
                            <v-card-subtitle>{{ message.username }}</v-card-subtitle>
                        </v-icon>
                    </v-chip>
                </v-badge>
                <v-card
                    :color="props.message.author == userId ? 'primary':'indigo-lighten-1'"
                    class="rounded-xl"
                    max-width="300"
                    @click="props.message.img ? showFullImage : showTime"
                >
                    <v-dialog v-if="props.message.img" max-width="800">
                        <template v-slot:activator="{ props: activatorProps }">
                            <v-img
                                v-bind="activatorProps"
                                :src="props.message.img" 
                                :width="200" 
                                contain
                            >
                            </v-img>
                        </template>

                        <template v-slot:default="{ isActive }">
                            <v-card variant="elevated" elevation="24" color="primary" rounded="5">
                                <v-img
                                    :src="props.message.img" 
                                    cover
                                    class="text-right"
                                >
                                </v-img>
                                <v-card color="primary" rounded="0" class="pa-4 d-flex align-center justify-space-between">
                                    <v-card-subtitle class="font-weight-bold" opacity="10">{{ imageName }}</v-card-subtitle>
                                    <v-card-subtitle>{{timeInHMS }}</v-card-subtitle>
                                </v-card>
                            </v-card>
                        </template>
                    </v-dialog>
                    
                    <v-card-text v-else class="py-2" @click="showTime">{{ props.message.text }}</v-card-text>
                </v-card>
                <v-card-subtitle v-if="time" class="d-flex justify-center align-center">{{ timeInHMS }}</v-card-subtitle>
            </v-col>

            <v-col
                v-if="props.message.img && props.message.text"
                cols="12"
                :class="props.message.author == userId ? 'mt-n5 d-flex justify-end':'mt-n5 ml-14 d-flex justify-start'"
            >
                <v-card
                    :color="props.message.author == userId ? 'primary':'indigo-lighten-1'"
                    class="rounded-xl pa-0 ma-0"
                    max-width="300"
                >
                    <v-card-subtitle class="py-2">{{ props.message.text }}</v-card-subtitle>
                </v-card>
            </v-col>
        </v-row>
    </div>
</template>

<script setup>
    import authentication from '~/composables/auth'

    const props = defineProps({
        message: Object
    })

    const { userId } = authentication()

    const time = ref(false)
    const showTime = () => {
        time.value = !time.value
    }

    const timeInHMS = computed(() => {
        const date = new Date(props.message.time)
        const locale = navigator.language || 'en-US'

        const options = {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true, // Use 12-hour format (AM/PM), set to false for 24-hour format
        }

        return new Intl.DateTimeFormat(locale, options).format(date)
    })

    const imageName = computed(() => {
        return props.message.img.split("?")[0].split("-").pop()
    })
</script>