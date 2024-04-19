import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.data('navbar', (user) => ({
        signedIn: false,
        user: null,
        userFullName: null,
        userRole: null,
        init() {
            console.log(user);
            if (user !== undefined) {
                this.signedIn = true;
                this.userFullName = user.Name + ' ' + user.Patronymic + ' ' + user.Surname;
                this.userRole = user.Role;
            }
        },

        logOut(){
            const baseUrl = window.location.origin;
            axios.get(`${baseUrl}/auth/logout`)
            .then(response => {
                if (response.status === 200) {
                    this.signedIn = false;
                    Alpine.store('userStore').currentUser = null;
                    Alpine.store('userStore').currentRole = Roles.NONE;
                    window.location.href = `${baseUrl}/login?logged_out=true`;
                }
            })
            .catch(error => {
                console.log(error);
                createToast('error', 'There was an error logging out');
                setTimeout(() => {
                    removeToast();
                }, 3000);
            });
        }
    }));
});