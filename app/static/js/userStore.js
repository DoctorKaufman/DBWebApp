document.addEventListener('alpine:init', () => {

    const Roles = {
        NONE: 'NONE',
        MANAGER: 'MANAGER',
        CASHIER: 'CASHIER',
    };

    window.Roles = Roles;

    Alpine.store('tableState', {
        currentUser : null,
        currentRole : Roles.NONE,
    });
});