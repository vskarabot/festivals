<template>
    <!-- TODO UNIMPORTANT - if time reorganize code as right now this is completely identical to -->
    <!-- the one in Components/PostDetail but just using different script functions -->
    <!-- (only the post detail, at the end there is some new code) -->
    <v-sheet v-if="post" color="primary">
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

        <v-card class="mx-auto" max-width="500" variant="flat" color="primary" rounded="0">
            <v-row>
                <v-col cols="10" class="d-flex align-center pl-7 pt-6 pb-0">
                    <NuxtLink :to="{ name: 'festivals-id', params: { id: `${post.festival}`} }">
                        <v-chip
                            :variant="hoverFestName ? 'elevated' : 'text'"
                            color="teall1"
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
                </v-col>
                <v-col cols="2" class="d-flex align-center justify-end pt-6 pr-6 pb-0">
                    <v-icon class="ml-2" icon="mdi-dots-vertical" @click.prevent="showBottomSheet = true"></v-icon>
                </v-col>
            </v-row>
            <v-row class="mt-4 mb-1">
                <v-col class="d-flex align-center pl-4 pt-0">
                    <v-chip variant="text" size="small">
                        <v-icon icon="mdi-account" class="mr-1"></v-icon>
                        {{ user }}
                    </v-chip>
                    <ChipLabel :label="post.label" />
                </v-col>
            </v-row>

            <v-card-title>{{ post.title }}</v-card-title>
            <v-card-text>{{ post.text }}</v-card-text>
            <v-card-actions>
                <v-btn 
                    :color="post.user_likes ? 'blue-darken-2' : (hoverLike ? 'white' : 'card')" 
                    size="small" 
                    rounded 
                    variant="flat"
                    :prepend-icon="post.user_likes ? 'mdi-thumb-up' : 'mdi-thumb-up-outline'"
                    @click.prevent="reaction('like')"
                    @mouseover="hoverLike = true"
                    @mouseleave="hoverLike = false"
                    @mousedown="hoverLike = false"
                >
                    {{ post.number_of_likes }}
                </v-btn>
                
                <v-btn 
                    :color="post.user_dislikes ? 'red' : (hoverDislike ? 'white' : 'card')" 
                    size="small" 
                    rounded 
                    variant="flat"
                    :prepend-icon="post.user_dislikes ? 'mdi-thumb-down' : 'mdi-thumb-down-outline'"
                    @click.prevent="reaction('dislike')"
                    @mouseover="hoverDislike = true"
                    @mouseleave="hoverDislike = false"
                    @mousedown="hoverDislike = false"
                >
                    {{ post.number_of_dislikes }}
                </v-btn>
            </v-card-actions>
            <!-- to here, from here on its new code -->

            <v-text-field v-if="!textArea" @click="textArea = true" label="Write a comment..." variant="outlined"
                density="compact" single-line rounded class="mt-2 px-2" />
            <v-textarea v-model="newComment" v-else variant="outlined" rounded="xl" class="mx-2 px-2" color="teall1" autofocus></v-textarea>
            <v-row v-if="textArea">
                <v-col class="d-flex justify-end pt-0 pb-6">
                    <v-btn rounded @click="textArea = false" color="warning">
                        Cancel
                    </v-btn>
                    <v-btn :disabled="newComment.length < 1" @click="addComment" rounded color="teall1" class="mr-4 ml-2">
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
                        color="teall1"
                        density="compact"
                        rounded
                        class="px-2"
                        @update:modelValue="fetchComments"
                    ></v-select>
                </v-col>
            </v-row>

            <v-divider thickness="3"></v-divider>

            <v-card-title>Comments</v-card-title>
            <v-card v-if="comments && comments.length" v-for="(comment, index) in comments" color="primary" variant="flat">
                <Comment @new-comment="updateCommentRef" :key="comment.id" :index="index" :comment="comment" :level="level" />
            </v-card>
            <v-sheet v-else class="ml-4">
                No comments yet
            </v-sheet>

        </v-card>
    </v-sheet>
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
const hoverFestName = ref(false)

const hoverLike = ref(false)
const hoverDislike = ref(false)

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

onActivated(() => {
    hoverFestName.value = false
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
