<template>
    <v-sheet class="mx-auto" max-width="500">
        <v-divider></v-divider>
        
        <v-bottom-sheet v-model="showBottomSheet" inset="true">
            <v-list>
                <v-list-item
                    prepend-icon="mdi-bookmark"
                    title="Save"
                    @click="showBottomSheet = false"
                ></v-list-item>
                <v-list-item
                    prepend-icon="mdi-pencil"
                    title="Edit"
                    @click="edit"
                ></v-list-item>
                <v-list-item
                    prepend-icon="mdi-delete"
                    title="Delete"
                    @click="emitEvent('delete')"
                ></v-list-item>
            </v-list>
        </v-bottom-sheet>
        
        <v-card :to="`/forum/${props.post.festival}/post/${props.post.id}`" class="mx-auto" variant="flat">
            <template v-slot:prepend>
                <v-chip
                    variant="text"
                    class="ma-0 pa-0"
                >
                    <v-icon icon="mdi-account" class="mr-1"></v-icon>
                    {{ user }}
                    <span class="mx-2">•</span>
                </v-chip>

                <v-card-subtitle class="my-0 py-0">{{ post.festival_name }}, Today</v-card-subtitle>
            </template>
            <template v-slot:append>
                <v-chip                 
                    :color="getColor(post.label)"
                    size="small"
                >
                    {{ post.label }}
                </v-chip>
                <v-icon class="ml-2" icon="mdi-dots-horizontal" @click.prevent="showBottomSheet=true"></v-icon>
            </template>
            <v-card-title>{{ post.title }}</v-card-title>
            <v-card-text>{{ post.text }}</v-card-text>
            <v-card-actions>
                <v-btn size="small" rounded variant="tonal" @click.prevent="emitEvent('like')"><v-icon icon="mdi-thumb-up" />{{ post.number_of_likes }}</v-btn>
                <v-btn size="small" rounded variant="tonal" @click.prevent="emitEvent('dislike')"><v-icon icon="mdi-thumb-down" />{{ post.number_of_dislikes }}</v-btn>
                <v-btn size="small" @click.prevent="openPost" variant="tonal" rounded prepend-icon="mdi-comment">Comments</v-btn>
                <v-btn size="small" rounded variant="tonal" @click.prevent="edit" v-if="post.is_author"><v-icon icon="mdi-pencil" /></v-btn>
                <v-btn size="small" rounded variant="tonal" @click.prevent="emitEvent('delete')" v-if="post.is_author || post.can_delete"><v-icon icon="mdi-delete" /></v-btn>
            </v-card-actions>
        </v-card>
    </v-sheet>
</template>

<script setup>

    const props = defineProps({
        post: Object,
        index: Number
    })

    const showBottomSheet = ref(false)

    const emit = defineEmits(['like', 'dislike', 'delete'])

    const emitEvent = (action) => {
        emit(action, props.post.id, props.index)
    }

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

    const user = computed(() => {
        return props.post.is_author ? 'Me' : props.post.username
    })

    const openPost = () => {
        useRouter().push({
            name: 'forum-id-post-pid',
            params: { id: props.post.festival, pid: props.post.id }
        })
    }

    const edit = () => {
        showBottomSheet.value = false

        useRouter().push({
            name: 'forum-id-post-pid-edit',
            params: { id: props.post.festival, pid: props.post.id }
        })
    }
</script>