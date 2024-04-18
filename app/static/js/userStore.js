document.addEventListener('alpine:init', () => {

    const Roles = {
        NONE: 'NONE',
        MANAGER: 'MANAGER',
        CASHIER: 'CASHIER',
    };

    window.Roles = Roles;

    Alpine.store('userStore', {
        currentUser : null,
        currentRole : Roles.NONE,
    });
});