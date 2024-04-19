<template>
    <p>{{ message }}</p>
    <NuxtLink to="/auth/login/" v-if="success">Login</NuxtLink>
</template>

<script>
    definePageMeta({
        layout: 'blank'
    })

    import * as requests from '../../../../services/requests'

    export default {
        data () {
            return {
                message: 'Activating account...',
                uid: '',
                token: '',
                success: false,
            }
        },
        // this page opens by itself, sents request and if all ok activates account (Djoser)
        async mounted () {
            this.uid = this.$route.params.uid
            this.token = this.$route.params.token

            const responseData = await requests.activate(this.uid, this.token)

            const status = responseData.status

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