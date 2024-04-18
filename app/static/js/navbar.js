import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', (user) => {
    Alpine.data('navbar', () => ({
        signedIn: false,
        user: user,
        init() {
            if (this.user !== null) {
                this.signedIn = true;
            }
            Alpine.store('userStore').currentUser = this.user;
            Alpine.store('userStore').currentRole = this.user.Role === 'Manager' ?
                Roles.MANAGER : Roles.CASHIER;
        },
    }));
});