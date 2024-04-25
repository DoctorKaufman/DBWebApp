document.addEventListener('alpine:init', () => {
    Alpine.data('receiptsInteractions', (activeTab, receipts, user) => ({
        activeTab: activeTab,
        receipts: receipts,
        user: user,

        init() {
            Alpine.store('receiptsState').receipts = receipts;
        }
    }));
});