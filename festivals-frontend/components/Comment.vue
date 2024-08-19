<template>
    <v-card :class="`mx-auto ml-${level * 4} my-2 pb-2`" variant="flat" :color="level > 0 ? 'card' : 'secondary'" max-width="500" rounded="xl">
        <template v-slot:prepend>
            <v-chip variant="text" class="ma-0 pa-0">
                <v-icon icon="mdi-account" class="mr-1"></v-icon>
                {{ comment.is_author ? 'Me' : comment.username }}
                <span class="mx-2">•</span>
            </v-chip>

            <v-card-subtitle v-if="!comment.deleted" class="my-0 py-0">{{ comment.time_string }}</v-card-subtitle>
            <v-card-subtitle v-else class="my-0 py-0">(deleted)</v-card-subtitle>
        </template>


        <v-bottom-sheet v-model="showBottomSheet" inset>
            <v-list>
                <v-list-item
                    prepend-icon="mdi-delete"
                    title="Delete"
                    @click="deleteComment"
                ></v-list-item>
            </v-list>
        </v-bottom-sheet>
        <template v-slot:append>
            <v-icon v-if="!comment.deleted && comment.is_author || comment.can_delete" class="ml-2" icon="mdi-dots-horizontal" @click="showBottomSheet = true"></v-icon>
            <v-icon v-else-if="comment.deleted" class="ml-2" icon="mdi-trash-can-outline" color="error"></v-icon>
        </template>

        <v-divider thickness="1" color="primary" opacity="10"></v-divider>

        <v-card-text v-if="!comment.deleted">{{ props.comment.text }}</v-card-text>
        <v-card-text v-else>[The comment was removed]</v-card-text>
        <v-card-actions v-if="!comment.deleted">
            <v-btn 
                :color="props.comment.user_likes ? 'blue-darken-2' : (hoverLike ? 'white': 'card')" 
                size="small" 
                rounded 
                variant="flat" 
                :prepend-icon="props.comment.user_likes ? 'mdi-thumb-up' : 'mdi-thumb-up-outline'"
                @click="action('like')"
                @mouseover="hoverLike = true"
                @mouseleave="hoverLike = false"
                @mousedown="hoverLike = false"
            >
                {{ props.comment.number_of_likes }}
            </v-btn>
            
            <v-btn 
                :color="props.comment.user_dislikes ? 'red' : (hoverDislike ? 'white' : 'card')" 
                size="small" 
                rounded 
                variant="flat"
                :prepend-icon="props.comment.user_dislikes ? 'mdi-thumb-down' : 'mdi-thumb-down-outline'"
                @click="action('dislike')"
                @mouseover="hoverDislike = true"
                @mouseleave="hoverDislike = false"
                @mousedown="hoverDislike = false"
            >
                {{ props.comment.number_of_dislikes }}
            </v-btn>
            
            <v-btn
                size="small"
                :color="hoverReply ? 'white' : 'card'" 
                rounded 
                variant="flat"
                prepend-icon="mdi-reply"
                @click="reply = true"
                @mouseover="hoverReply = true"
                @mouseleave="hoverReply = false"
                @mousedown="hoverReply = false"
            >
            </v-btn>
        </v-card-actions>

        <!-- reply textarea -->
        <v-textarea v-if="reply" v-model="replyText" variant="outlined" rounded class="mx-2" color="teall1"></v-textarea>
        <v-row v-if="reply">
            <v-col class="d-flex justify-end pt-0 mr-2">
                <v-btn @click="reply = false" rounded variant="flat" color="warning">
                    Cancel
                </v-btn>
                <v-btn :disabled="replyText.length < 1" @click="replyToComment" rounded variant="flat" color="teall1" class="ml-2">
                    Comment
                </v-btn>
            </v-col>
        </v-row>
    </v-card>
    <v-chip 
        size="small" 
        v-if="comment.child_comments.length"
        @click="toggleReplies" 
        :class="`mx-auto ml-${level * 4} my-1`" 
        color="teall1"
        :text="showReplies === true ? 'Show less' : 'Show more'"
    >
    </v-chip>

    <!-- recursive component -->
    <div v-if="comment.child_comments && comment.child_comments.length && showReplies">
        <Comment v-for="(childComment, childIndex) in comment.child_comments"
            @new-comment="updateCommentRef"
            :key="childComment.id"
            :index="childIndex"
            :comment="childComment"
            :level="level + 1" />
    </div>
</template>

<script setup>
    import * as requests from '../services/requests'

    const props = defineProps({
        comment: Object,
        level: Number
    })

    // for both if delete or update
    const emit = defineEmits(['new-comment'])

    const showReplies = ref(false)
    const showBottomSheet = ref(false)
    const reply = ref(false)
    const replyText = ref('')

    const hoverLike = ref(false)
    const hoverDislike = ref(false)
    const hoverReply = ref(false)

    onMounted(async() => {
        showReplies.value = props.level < 1 ? true : false
    })

    const toggleReplies = () => {
        showReplies.value = !showReplies.value
    }

    const deleteComment = async() => {
        const response = await requests.quazyDeleteComment(props.comment.id)
        showBottomSheet.value = false  

        emit('new-comment')
    }

    const action = async(action) => {
        const response = await requests.likeComment(props.comment.id, action)
        const responseData = await response.json()
        props.comment.user_likes = responseData.user_likes
        props.comment.user_dislikes = responseData.user_dislikes
        props.comment.number_of_likes = responseData.number_of_likes
        props.comment.number_of_dislikes = responseData.number_of_dislikes
    }

    const replyToComment = async() => {
        const response = await requests.addComment(props.comment.post, replyText.value, props.comment.id)
        replyText.value = ''
        reply.value = false

        // if level 1 we need to emit to parent component (index.vue) as its first called there - to update whole comment section
        emit('new-comment')
    }

    // else - we emit forward up to parent -> then it updates ? as im only calling new data request in index -> might be worth changing to load in each comment component for less data transfering
    const updateCommentRef = async() => {
        emit('new-comment')
    }
</script>