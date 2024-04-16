<template>
    <div>
        <form @submit.prevent="register" v-if="!success">
            <input type="text" placeholder="First name" v-model="fName"></input>
            <input type="text" placeholder="Last name" v-model="lName"></input>
            <input type="text" placeholder="username" v-model="username"></input>
            <input type="password" placeholder="Password" v-model="password"></input>
            <input type="" placeholder="Confirm password" v-model="confirmPassword"></input>
            <input type="email" placeholder="e-mail address" v-model="email"></input>
            <input type="date" v-model="birthDate"></input>
            <input type="radio" name="gender" value="M" v-model="selectedGender">Male <input type="radio" name="gender" value="F" v-model="selectedGender"> Female
            <select v-model="country">
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

    export default {
        data () {
            return {
                fName: '',
                lName: '',
                email: '',
                birthDate: '',
                selectedGender: 'M',
                country: '',

                success: false,
            }
        },
        methods: {
            async register () {
                const res = await fetch('http://localhost:8000/auth/users/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        first_name: this.fName,
                        last_name: this.lName,
                        username: this.username,
                        email: this.email,
                        password: this.password,
                        date_of_birth: this.birthDate,
                        country: this.country,
                        gender: this.selectedGender,
                    })
                })

                const data = await res.json()
                console.log(data)

                if (data.id) {
                    this.success = true
                }
            },
            async resend () {
                const res = await fetch('http://localhost:8000/auth/users/resend_activation/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.email
                    })
                })

                
            }
        }
    }
</script>
