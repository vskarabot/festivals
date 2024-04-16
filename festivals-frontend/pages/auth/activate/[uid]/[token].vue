<template>
    <p>{{ message }}</p>
    <NuxtLink to="/auth/login/" v-if="success">Login</NuxtLink>
</template>

<script>
    definePageMeta({
        layout: 'blank'
    })

    export default {
        data () {
            return {
                message: 'Activating account...',
                uid: '',
                token: '',
                success: false,
            }
        },
        async mounted () {
            this.uid = this.$route.params.uid
            this.token = this.$route.params.token

            const res = await fetch('http://localhost:8000/auth/users/activation/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    uid: this.uid,
                    token: this.token
                })
            })

            const status = res.status

            // if no content -> success
            if (status === 204) {
                this.message = 'Account successfully activated'
                this.success = true
            }
            // if detail -> 403 forbidden (token expired or already activated) -> resend email?
            else {
                this.message = 'Token expired'
            }
            // if 400 bad request (data missing) -> dont think this can actually happen if body of request is correct
            
        }
    }
</script>