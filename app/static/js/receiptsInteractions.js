document.addEventListener('alpine:init', () => {
    Alpine.data('receiptsInteractions', (activeTab, user) => ({
        activeTab: activeTab,
        user: user,
    }));
});