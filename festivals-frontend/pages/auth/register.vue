<template>
    <div>
        <form @submit.prevent="register" v-if="!success">
            <input type="text" placeholder="First name" v-model="credentials.fName"></input>
            <input type="text" placeholder="Last name" v-model="credentials.lName"></input>
            <input type="text" placeholder="username" v-model="credentials.username"></input>
            <input type="password" placeholder="Password" v-model="credentials.password"></input>
            <input type="" placeholder="Confirm password" v-model="credentials.confirmPassword"></input>
            <input type="email" placeholder="e-mail address" v-model="credentials.email"></input>
            <input type="date" v-model="credentials.birthDate"></input>
            <input type="radio" name="gender" value="M" v-model="credentials.selectedGender">Male <input type="radio" name="gender" value="F" v-model="selectedGender"> Female
            <select v-model="credentials.country">
                <option value="SI">Slovenia</option>
                <option value="US">USA</option>
            </select>
            <button type="submit">Register</button>
        </form>
        <p v-if="!success">Already have an account? <NuxtLink to="/auth/login">Login</NuxtLink></p>
        <p v-if="success">Account successfully created. Email was sent to {{ email }} to activate the account. </p>
        <p v-if="success">Didn't get the email? <button @click="resend">Resend</button></p>
    </div>
</template>

<script>
    definePageMeta({
        layout: 'blank'
    })

    import * as requests from '../services/requests'

    export default {
        data () {
            return {
                credentials: {
                    fName: '',
                    lName: '',
                    email: '',
                    birthDate: '',
                    selectedGender: 'M',
                    country: '',
                },
                success: false,
            }
        },
        methods: {
            async register () {
                const responseData = await requests.register(this.credentials)
                if (responseData === true) {
                    this.success = true
                }
            },
            async resend () {
                await requests.resend(this.credentials.email)                
            }
        }
    }
</script>
