import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.data('loginForm', () => ({

        user: null,

        loginRequest() {
            const baseUrl = window.location.origin;
            console.log(baseUrl);
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
                // window.location.href = `${baseUrl}/`;
                createToast('success', `Login successful. Welcome, ${data.username}!`);
            })
            .catch(error => {
                console.error('Request failed:', error);
                createToast('error', 'Invalid credentials');
            });
        },
    }));
});