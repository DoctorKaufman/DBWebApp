import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.data('loginForm', () => ({

        user: null,

        init() {
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('logged_out') === 'true') {
                createToast('success', 'You have been logged out');
            }
        },

        loginRequest() {
            const baseUrl = window.location.origin;
            const login = document.getElementById('login').value;
            const password = document.getElementById('password').value;



            const data = {
                "login": login,
                "password": password,
            };
            console.log(data);
            console.log(`${baseUrl}/auth/login`);
            axios.post(`${baseUrl}/auth/login`, data)
            .then(response => {
                const data = response.data;
                this.user = data;
                Alpine.store('userStore').currentUser = data;
                data.position === 'manager' ? 
                Alpine.store('userStore').currentRole = Roles.MANAGER : 
                Alpine.store('userStore').currentRole = Roles.CASHIER;
                window.location.href = `${baseUrl}/?logged_in=true&username=${data.username}`;

                // const value = `; ${response.cookie}`;
                // const parts = value.split(`; user=`);
                // if (parts.length === 2) {
                //     console.log(parts.pop().split(';').shift());
                // }
            })
            .catch(error => {
                console.error('Request failed:', error);
                createToast('error', 'Invalid credentials');
            });
        },

    }));
});