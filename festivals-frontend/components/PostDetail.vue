<template>
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
        
        <v-card
            max-width="500"
            :to="`/forum/${props.post.festival}/post/${props.post.id}`" 
            class="mx-auto mb-4" 
            variant="flat" 
            rounded="xl" 
            color="secondary"
        >
            <v-row>
                <v-col cols="10" class="d-flex align-center pl-7 pt-6 pb-0">
                    <NuxtLink :to="{ name: 'festivals-id', params: { id: `${post.festival}`} }">
                        <v-chip
                            :variant="hoverFestName ? 'elevated' : 'text'"
                            :color="hoverFestName ? 'warning' : 'teall1'"
                            :class="hoverFestName ? 'px-2' : 'px-0'"
                            rounded="md"
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
                </v-col>
                <v-col cols="2" class="d-flex align-center justify-end pt-6 pr-6 pb-0">
                    <v-icon @click.prevent="showBottomSheet=true" icon="mdi-dots-vertical"></v-icon>
                </v-col>
            </v-row>
            <v-row class="mt-4">
                <v-col class="d-flex align-center pl-4 pt-0">
                    <v-chip
                        size="small"
                        color="white"
                        variant="text"
                    >
                        <v-icon icon="mdi-account"></v-icon>
                        {{ user }}
                    </v-chip>
                    <ChipLabel :label="post.label"/>
                </v-col>
                <v-divider thickness="2" color="primary" opacity="10"></v-divider>
            </v-row>
            
            <v-card-title class="my-2">{{ post.title }}</v-card-title>
            <v-card-text>{{ post.text }}</v-card-text>
            <v-card-actions>
                <v-btn 
                    v-if="post.user_likes" 
                    color="blue-darken-2" 
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
                    :color="hoverLike ? 'white' : 'card'"
                    variant="flat"
                    rounded
                    prepend-icon="mdi-thumb-up-outline" 
                    @click.prevent="emitEvent('like')"
                    @mouseover="hoverLike = true"
                    @mouseleave="hoverLike = false"
                    @mousedown="hoverDislike = false"
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
                    :color="hoverDislike ? 'white' : 'card'"
                    variant="flat"
                    rounded
                    prepend-icon="mdi-thumb-down-outline" 
                    @click.prevent="emitEvent('dislike')"
                    @mouseover="hoverDislike = true"
                    @mouseleave="hoverDislike = false"
                    @mousedown="hoverDislike = false"
                >
                {{ post.number_of_dislikes }}
                </v-btn>
                
                <v-btn width="100" size="small" color="card" variant="flat" @click.prevent="openPost" rounded prepend-icon="mdi-comment-outline">{{ post.number_of_comments }}</v-btn>
            </v-card-actions>
        </v-card>
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