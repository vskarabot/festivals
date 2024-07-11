<template>
    <!-- TODO UNIMPORTANT - if time reorganize code as right now this is completely identical to -->
    <!-- the one in Components/PostDetail but just using different script functions -->
    <!-- (only the post detail, at the end there is some new code) -->
    <div v-if="post">
        <v-sheet class="mx-auto" max-width="500">
            <v-divider></v-divider>

            <v-bottom-sheet v-model="showBottomSheet" inset>
                <v-list>
                    <v-list-item prepend-icon="mdi-bookmark" title="Save"
                        @click="showBottomSheet = false"></v-list-item>
                    <v-list-item v-if="post.is_author" prepend-icon="mdi-pencil" title="Edit"
                        @click="edit"></v-list-item>
                    <v-list-item v-if="post.is_author || post.can_delete" prepend-icon="mdi-delete" title="Delete"
                        @click="deletePost"></v-list-item>
                </v-list>
            </v-bottom-sheet>

            <v-card class="mx-auto" variant="flat">
                <template v-slot:prepend>
                    <v-chip variant="text" class="ma-0 pa-0">
                        <v-icon icon="mdi-account" class="mr-1"></v-icon>
                        {{ user }}
                        <span class="mx-2">•</span>
                    </v-chip>

                    <v-card-subtitle class="my-0 py-0">{{ post.festival_name }}, {{ post.time_string }}<span
                            v-if="post.edited">&nbsp;(edited)</span></v-card-subtitle>
                </template>
                <template v-slot:append>
                    <ChipLabel :label="post.label" />
                    <v-icon class="ml-2" icon="mdi-dots-horizontal" @click.prevent="showBottomSheet = true"></v-icon>
                </template>
                <v-card-title>{{ post.title }}</v-card-title>
                <v-card-text>{{ post.text }}</v-card-text>
                <v-card-actions>
                    <v-btn v-if="post.user_likes" color="primary" size="small" rounded variant="tonal" @click.prevent="reaction('like')"><v-icon icon="mdi-thumb-up" />{{ post.number_of_likes }}</v-btn>
                    <v-btn v-else size="small" color="blue-grey-darken-1" rounded variant="tonal" @click.prevent="reaction('like')"><v-icon icon="mdi-thumb-up-outline" />{{ post.number_of_likes }}</v-btn>
                    
                    <v-btn v-if="post.user_dislikes" color="red" size="small" rounded variant="tonal" @click.prevent="reaction('dislike')"><v-icon icon="mdi-thumb-down" />{{ post.number_of_dislikes }}</v-btn>
                    <v-btn v-else size="small" color="blue-grey-darken-1" rounded variant="tonal" @click.prevent="reaction('dislike')"><v-icon icon="mdi-thumb-down-outline" />{{ post.number_of_dislikes }}</v-btn>
                </v-card-actions>
                <!-- to here, from here on its new code -->

                <v-text-field v-if="!textArea" @click="textArea = true" label="Write a comment..." variant="outlined"
                    density="compact" single-line rounded class="mt-2" />
                <v-textarea v-model="newComment" v-else variant="outlined" rounded></v-textarea>
                <v-row v-if="textArea">
                    <v-col class="d-flex justify-end pt-0">
                        <v-btn rounded variant="tonal" @click="textArea = false">
                            Cancel
                        </v-btn>
                        <v-btn @click="addComment" rounded color="primary" class="ml-2">
                            Comment
                        </v-btn>
                    </v-col>
                </v-row>
                <v-row v-else>
                    <v-col cols="6">
                        <v-select 
                            v-model="sort"
                            label="Sort by" 
                            :items="['Top', 'New']" 
                            variant="outlined" 
                            density="compact"
                            rounded
                            @update:modelValue="fetchComments"
                        ></v-select>
                    </v-col>
                </v-row>
            </v-card>

            <v-card-title>Comments</v-card-title>
            <v-divider></v-divider>
            <v-sheet v-if="comments && comments.length" v-for="(comment, index) in comments">
                <Comment @new-comment="updateCommentRef" :key="comment.id" :index="index" :comment="comment" :level="level" />
            </v-sheet>
            <v-sheet v-else class="ml-4">
                No comments yet
            </v-sheet>
        </v-sheet>
    </div>
</template>

<script setup>
// single post (when finished try to join with some other codes)
import * as requests from '../../../../../services/requests'

const post = ref(null)
const comments = ref(null)
const level = ref(0)

const sort = ref('New')

const showBottomSheet = ref(false)
const textArea = ref(false)

const newComment = ref('')

const fetchComments = async() => {
    const params = makeParams()
    const response2 = await requests.getComments(post.value.id, params)
    comments.value = response2
}

onMounted(async () => {
    const response = await requests.getPostDetail(useRoute().params.pid)
    const responseData = await response.json()
    post.value = responseData

    await fetchComments()
})

const reaction = async (action) => {
    const response = await requests.likePost(useRoute().params.pid, action)

    if (response.status === 200) {
        const responseData = await response.json()
        post.value = responseData
    }
}

const deletePost = async () => {
    showBottomSheet.value = false

    const response = await requests.deletePost(useRoute().params.pid)

    if (response.status === 204) {
        useRouter().replace({
            name: 'forum-id',
            params: { id: post.value.festival }
        })
    }
}

const edit = () => {
    showBottomSheet.value = false

    useRouter().push({
        name: 'forum-id-post-pid-edit',
        params: { id: post.value.festival, pid: post.value.id }
    })
}

const user = computed(() => {
    return post.value.is_author ? 'Me' : post.value.username
})

const addComment = async() => {
    const response = await requests.addComment(post.value.id, newComment.value)
    textArea.value = false

    fetchComments()
}

const updateCommentRef = async() => {
    fetchComments()
}

const makeParams = () => {
    return `?sort=${sort.value}`
}
</script>
