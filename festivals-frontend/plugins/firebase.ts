import { initializeApp } from 'firebase/app'
import { getStorage } from 'firebase/storage'

export default defineNuxtPlugin(nuxtApp => {
    const firebaseConfig = {
        apiKey: "AIzaSyBmsg5g8W5PRDX4SJN_fw4TUFGr1__sQAs",      
        authDomain: "festivals-c4296.firebaseapp.com",      
        projectId: "festivals-c4296",      
        storageBucket: "festivals-c4296.appspot.com",      
        messagingSenderId: "183368271365",      
        appId: "1:183368271365:web:c187574254125885547e6c",      
        measurementId: "G-JMCNT2FJLL"      
      };

    const app = initializeApp(firebaseConfig)
    const storage = getStorage(app)

    nuxtApp.provide('firebase', app)
    nuxtApp.provide('storage', storage)
})