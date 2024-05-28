<template>
    <div>
        <form>
            <input type="text" placeholder="Title" v-model="post.title"></input><br>
            <textarea placeholder="Text" v-model="post.text"></textarea><br>
            <select v-model="post.label">
                <option value="travel">Travel</option>
                <option value="lineup">Lineup</option>
                <option value="tips">Tips</option>
                <option value="shitpost">Shitpost</option>
            </select><br>
        </form>
    </div>
</template>

<script setup>
    const props = defineProps(['post'])
</script>