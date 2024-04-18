import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.data('navbar', (user) => ({
        user: user,
        notSignedIn: user == undefined,
        isManager: user?.position === 'manager',
        init() {
            console.log(this.user);
            console.log(this.notSignedIn);
            console.log(this.isManager);
        },
    }));
});