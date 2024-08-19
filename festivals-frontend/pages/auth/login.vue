<template>
    <v-sheet color="primary">
        <v-sheet
            class="pa-4 text-center mx-auto"
            max-width="600"
            rounded="lg"
            width="100%"
            color="primary"
        >
            <v-card class="mx-auto px-8 py-8" color="secondary">
                <v-alert
                    v-if="errorMessage"
                    class="mb-4"
                    color="error"
                    variant="flat"
                    closable
                >
                {{ errorMessage }}
                </v-alert>
                <h1>Welcome!</h1>
                <br>
                <v-form @submit.prevent="login" v-model="formValid">
                    <v-text-field 
                        v-model="credentials.usernameOrEmail" 
                        :rules="[rules.required]"
                        label="Username or email" 
                        clearable 
                        variant="outlined"
                        color="teall1"
                    >
                    </v-text-field>
                    <v-text-field 
                        :type="normalTextPass ? 'text' : 'password'"
                        :rules="[rules.required]"
                        v-model="credentials.password"
                        label="Password"  
                        variant="outlined"
                        color="teall1"
                        :append-inner-icon="normalTextPass ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append-inner="normalTextPass = !normalTextPass"
                    >
                    </v-text-field>
                    <v-btn :disabled="!formValid" type="submit" color="teall1" class="d-block mx-auto mt-4">LOGIN</v-btn>

                    <br>
                    <p class="text-center">Don't have an account? <NuxtLink to="/auth/register">Sign-in</NuxtLink></p>
                </v-form>
            </v-card>
        </v-sheet>
    </v-sheet>
</template>

<script setup>
definePageMeta({
    layout: 'blank'
})
import * as requests from '../services/requests'
    
    const credentials = ref({
        usernameOrEmail: '',
        password: ''
    })

    const normalTextPass = ref(false)
    const errorMessage = ref('')
    const formValid = ref(false)

    /* DJANGO DEFAULTS
        - A password can’t be too similar to the users other personal information.
        - A password must contain at least 8 characters.
        - A password can’t be a commonly used password.
        - A password can’t be entirely numeric.
    */
    const rules = {
        required: value => !!value || 'Required.',
    }

    // responseData only if error i think
    const login = async () => {
        if (credentials.value.password && credentials.value.password) {
            const responseData = await requests.login(credentials.value)
            errorMessage.value = `${responseData}!`
        }
    }
</script>

