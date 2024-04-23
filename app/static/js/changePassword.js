import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.data('changePassword', (user) => ({
        user: user,
        newPassword: null,
        confirmPassword: null,
        newPasswordField: document.getElementById('newPassword'),
        confirmPasswordField: document.getElementById('confirmPassword'),

        submitChangePassword(){
            if (this.matchingPasswords()) {
                this.changePasswordRequest();
            } else {
                this.confirmPasswordField.value = '';
                this.confirmPasswordField.classList.add('border-red-500');
                createToast("error", "Passwords do not match.");
            }
        },

        matchingPasswords() {
            this.newPassword = this.newPasswordField.value;
            this.confirmPassword = this.confirmPasswordField.value;
            return this.newPassword === this.confirmPassword;  
        },

        changePasswordRequest() {
            const baseUrl = window.location.origin;
            const data = {
                "Password": this.newPassword,
            };
            console.log(data);
            axios.put(`${baseUrl}/auth/update_password/${this.user.ID}`, data)
            .then(response => {
                const data = response.data;
                console.log(data);
                window.location.href = `${baseUrl}/?changed_password=true`;
            })
            .catch(error => {
                console.error('Request failed:', error);
                createToast('error', error.response.data.message);
            });
        },
    }));
});