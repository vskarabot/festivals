<template>
    <v-sheet
        class="pa-4 mx-auto"
        max-width="600"
        rounded="lg"
        width="100%"
    >
        <v-card class="mx-auto px-8 py-8">
            <v-card-title>Account already active!</v-card-title>
            <v-card-text><v-btn color="primary">Home</v-btn></v-card-text>
        </v-card>
    </v-sheet>   
</template>

<script>
    definePageMeta({
        layout: 'blank'
    })

    import * as requests from '../../../../services/requests'

    export default {
        data () {
            return {
                message: '',
                uid: '',
                token: '',
                success: false,
                email: ''
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
                this.message = 'Account successfully activated. Thank you for using this app.'
                this.success = true
                // TODO display on alert? -> then redirect
                // TODO didnt recieve email? ...
            }
            // if detail -> 403 forbidden (token expired or already activated)
            // TODO : change djoser backend so it returns user_activated...
            else {
                this.message = 'Already activated!'
            }
            // if 400 bad request (data missing) -> dont think this can actually happen if body of request is correct
        },
        methods: {
            
        }
    }
</script>