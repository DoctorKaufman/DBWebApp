import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.data('homePage', () => ({
        init() {
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('logged_in') === 'true') {
                const username = urlParams.get('username');
                createToast('success', `Login successful. Welcome, ${username}!`);
            }
            if (urlParams.get('changed_password') === 'true') {
                createToast('success', 'Password updated successfully.');
            }
        }
    }));
});