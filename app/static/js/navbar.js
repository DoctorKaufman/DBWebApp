import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.data('navbar', (user) => ({
        signedIn: user !== undefined,
        user: null,
        init() {
            if (this.signedIn) {
                this.user = user;
                Alpine.store('userStore').currentUser = user;
                
                user.position === 'manager' ? 
                Alpine.store('userStore').currentRole = Roles.MANAGER : 
                Alpine.store('userStore').currentRole = Roles.CASHIER;
            }
        },
    }));
});