<template>
    <v-sheet>
        <v-card :class="`mx-auto ml-${level * 4}`" variant="flat">
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
            </template>

            <v-card-text v-if="!comment.deleted">{{ props.comment.text }}</v-card-text>
            <v-card-text v-else>[The post was removed]</v-card-text>
            <v-card-actions v-if="!comment.deleted">
                <v-btn v-if="props.comment.user_likes" color="primary" size="small" rounded variant="tonal" @click="action('like')"><v-icon icon="mdi-thumb-up" />{{ props.comment.number_of_likes }}</v-btn>
                <v-btn v-else size="small" color="blue-grey-darken-1" rounded variant="tonal" @click="action('like')"><v-icon icon="mdi-thumb-up-outline" />{{ props.comment.number_of_likes }}</v-btn>
                
                <v-btn v-if="props.comment.user_dislikes" color="red" size="small" rounded variant="tonal" @click="action('dislike')"><v-icon icon="mdi-thumb-down" />{{ props.comment.number_of_dislikes }}</v-btn>
                <v-btn v-else size="small" color="blue-grey-darken-1" rounded variant="tonal" @click="action('dislike')"><v-icon icon="mdi-thumb-down-outline" />{{ props.comment.number_of_dislikes }}</v-btn>
                
                <v-btn size="small" color="blue-grey-darken-1" rounded variant="tonal" @click="reply = true"><v-icon icon="mdi-reply" /></v-btn>
            </v-card-actions>

            <!-- reply textarea -->
            <v-textarea v-if="reply" v-model="replyText" variant="outlined" rounded></v-textarea>
            <v-row v-if="reply">
                <v-col class="d-flex justify-end pt-0">
                    <v-btn @click="reply = false" rounded variant="tonal">
                        Cancel
                    </v-btn>
                    <v-btn :disabled="replyText.length < 1" @click="replyToComment" rounded color="primary" class="ml-2">
                        Comment
                    </v-btn>
                </v-col>
            </v-row>

            <v-chip v-if="comment.child_comments.length" size="small" variant="text" color="primary" class="mb-2" @click="toggleReplies">
                {{ showReplies ? '- Hide Replies' : '+ Show Replies' }}
            </v-chip>

            <v-divider></v-divider>
        </v-card>

        <!-- recursive component -->
        <div v-if="comment.child_comments && comment.child_comments.length && showReplies">
            <Comment v-for="(childComment, childIndex) in comment.child_comments" 
                @new-comment="updateCommentRef"
                :key="childComment.id"
                :index="childIndex" :comment="childComment" :level="level + 1" />
        </div>
    </v-sheet>
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