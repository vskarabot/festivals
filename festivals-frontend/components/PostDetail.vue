<template>
    <v-sheet class="mx-auto" max-width="500">
        <v-divider></v-divider>
        
        <v-bottom-sheet v-model="showBottomSheet" inset>
            <v-list>
                <v-list-item
                    prepend-icon="mdi-bookmark"
                    title="Save"
                    @click="showBottomSheet = false"
                ></v-list-item>
                <v-list-item
                    v-if="post.is_author"
                    prepend-icon="mdi-pencil"
                    title="Edit"
                    @click="edit"
                ></v-list-item>
                <v-list-item
                    v-if="post.is_author || post.can_delete"
                    prepend-icon="mdi-delete"
                    title="Delete"
                    @click="emitEvent('delete')"
                ></v-list-item>
            </v-list>
        </v-bottom-sheet>
        
        <v-card :to="`/forum/${props.post.festival}/post/${props.post.id}`" class="mx-auto" variant="flat" rounded="xl">
            <template v-slot:prepend>
                <v-chip
                    variant="text"
                    class="ma-0 pa-0"
                >
                    <v-icon icon="mdi-account" class="mr-1"></v-icon>
                    {{ user }}
                    <span class="mx-2">•</span>
                </v-chip>

                <v-card-subtitle class="my-0 py-0">
                    <NuxtLink :to="{ name: 'festivals-id', params: { id: `${post.festival}`} }">
                        <v-chip
                            :variant="hoverFestName ? 'elevated' : 'text'"
                            :color="hoverFestName ? 'purple-darken-4' : 'default'"
                            :class="hoverFestName ? 'px-2' : 'px-0'"
                            rounded="sm"
                            @mouseover="hoverFestName = true"
                            @mouseleave="hoverFestName = false"
                        >
                            {{ post.festival_name }}
                        </v-chip>
                    </NuxtLink>
                    <v-chip
                        variant="text"
                        class="px-0"
                        rounded="sm"
                    >
                        &nbsp;•&nbsp;{{ post.time_string }}<span v-if="post.edited">&nbsp;(edited)</span>
                    </v-chip>
                </v-card-subtitle>
            
            </template>
            <template v-slot:append>
                <ChipLabel :label="post.label" />
                <v-icon class="ml-2" icon="mdi-dots-horizontal" @click.prevent="showBottomSheet=true"></v-icon>
            </template>
            <v-card-title>{{ post.title }}</v-card-title>
            <v-card-text>{{ post.text }}</v-card-text>
            <v-card-actions>
                <v-btn 
                    v-if="post.user_likes" 
                    color="primary" 
                    size="small" 
                    rounded 
                    variant="elevated" 
                    prepend-icon="mdi-thumb-up" 
                    @click.prevent="emitEvent('like')"
                >
                {{ post.number_of_likes }}
                </v-btn>
                <v-btn 
                    v-else 
                    size="small" 
                    :color="hoverLike ? 'primary' : 'blue-grey-darken-1'"
                    :variant="hoverLike ? 'outlined' : 'tonal'" 
                    rounded
                    prepend-icon="mdi-thumb-up-outline" 
                    @click.prevent="emitEvent('like')"
                    @mouseover="hoverLike = true"
                    @mouseleave="hoverLike = false"
                >
                {{ post.number_of_likes }}
                </v-btn>
                
                <v-btn 
                    v-if="post.user_dislikes" 
                    color="red" 
                    size="small" 
                    rounded 
                    variant="elevated" 
                    prepend-icon="mdi-thumb-down" 
                    @click.prevent="emitEvent('dislike')"
                >
                {{ post.number_of_dislikes }}
                </v-btn>
                <v-btn 
                    v-else 
                    size="small" 
                    :color="hoverDislike ? 'red' : 'blue-grey-darken-1'"
                    :variant="hoverDislike ? 'outlined' : 'tonal'" 
                    rounded
                    prepend-icon="mdi-thumb-down-outline" 
                    @click.prevent="emitEvent('dislike')"
                    @mouseover="hoverDislike = true"
                    @mouseleave="hoverDislike = false"
                >
                {{ post.number_of_dislikes }}
                </v-btn>
                
                <v-btn width="100" size="small" color="blue-grey-darken-1" @click.prevent="openPost" variant="tonal" rounded prepend-icon="mdi-comment-outline">{{ post.number_of_comments }}</v-btn>
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
    const hoverLike = ref(false)
    const hoverDislike = ref(false)
    const hoverFestName = ref(false)

    const emit = defineEmits(['like', 'dislike', 'delete'])

    const emitEvent = (action) => {
        emit(action, props.post.id, props.index)
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