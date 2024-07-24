<template>
    <v-container>
        <v-dialog v-model="isDialogOpen" max-width="500" persistent>
            <v-card title="Success">
                <v-card-text>The verification e-mail was sent to {{ credentials.email }}. To continue open the link provided in the e-mail.</v-card-text>
                <v-card-text>Didn't recieve the e-mail? <v-btn color="warning" @click="resend">Resend</v-btn></v-card-text>
            </v-card>
        </v-dialog>

        <v-stepper :items="['Basic info', 'Tell us about yourself']">
            <template v-slot:item.1>
                <v-sheet
                    class="pa-4 text-center mx-auto"
                    max-width="600"
                    rounded="lg"
                    width="100%"
                >
                    <v-card class="mx-auto px-8 py-8">
                        <h1>Welcome!</h1>
                        <br>
                        <v-form @submit.prevent="register" v-model="isFormValid">
                            <v-text-field :rules="[rules.required]" maxlength="50" v-model="credentials.fName" label="First name" clearable variant="outlined"></v-text-field>
                            <v-text-field :rules="[rules.required]" maxlength="50" v-model="credentials.lName" label="Last name" clearable variant="outlined"></v-text-field>
                            <v-text-field :rules="[rules.required]" maxlength="30" v-model="credentials.username" label="Username" clearable variant="outlined"></v-text-field>
                            <v-text-field :rules="[rules.required]" type="email" v-model="credentials.email" label="E-mail" clearable variant="outlined"></v-text-field>
                            <v-text-field :rules="[rules.required]" type="password" v-model="credentials.password" label="Password" clearable variant="outlined"></v-text-field>
                            <v-text-field :rules="[rules.required, rules.passwordsMatching]" type="password" v-model="retypePassword" label="Confirm password" clearable variant="outlined"></v-text-field>
                            <v-text-field :rules="[rules.required]" type="date" :max="maxDate" v-model="credentials.birthDate" label="Select your day of birth" variant="outlined"></v-text-field>
                            <v-radio-group label="Gender:" inline v-model="credentials.selectedGender">
                                <v-radio label="Male" value="M"></v-radio>
                                <v-radio label="Female" value="F"></v-radio>
                            </v-radio-group>
                            <v-select
                                v-model="credentials.country"
                                label="Select your country of residence"
                                :items="countries"
                                item-title="text"
                                item-value="value"
                                single-line
                                variant="outlined"
                            >
                            </v-select>
                        </v-form>
                    </v-card>
                </v-sheet>
            </template>
            <template v-slot:item.2>
                <v-sheet
                    class="pa-4 text-center mx-auto"
                    max-width="600"
                    rounded="lg"
                    width="100%"
                >
                    <v-card class="mx-auto px-8 py-8">
                        <h1>Welcome!</h1>
                        <br>
                        <v-form @submit.prevent="register" v-model="isFormValid">
                            <v-btn :disabled="!isFormValid" type="submit" color="primary" class="d-block mx-auto">Register</v-btn>
    
                            <br>
                            <p class="text-center">Already registered? <NuxtLink to="/auth/login">Log-in</NuxtLink></p>
                        </v-form>
                    </v-card>
                </v-sheet>
            </template>
        </v-stepper>
    </v-container>
</template>

<script>
    import * as requests from '../services/requests'
    import { countries } from '../../constants/countries'

    export default { 
        data () {
            return {
                credentials: {
                    fName: '',
                    lName: '',
                    email: '',
                    birthDate: '2000-01-01',
                    selectedGender: 'M',
                    country: 'SI',
                },
                maxDate: '',
                rules: {
                    required: value => !!value || 'This field is required!',
                    passwordsMatching: value => this.credentials.password === this.retypePassword || "Passwords don't match!"
                },
                countries,
                isDialogOpen: false,
                isFormValid: false,
                retypePassword: ''
            }
        },
        methods: {
            async register () {
                
                const response = await requests.register(this.credentials)
                if (response.ok) {
                    const responseData = response.json()
                    console.log(responseData)
                }
                else {
                    // add error to field?
                    console.log("error", response)
                }
            },
            async resend () {
                await requests.resend(this.credentials.email)             
            }
        },
        mounted () {
            const eighteenYearsAgo = new Date();
            eighteenYearsAgo.setFullYear(eighteenYearsAgo.getFullYear() - 18);
            this.maxDate = eighteenYearsAgo.toISOString().split('T')[0]
        }
    }
</script>

<script setup>
    definePageMeta({
        layout: 'blank'
    })
</script>
