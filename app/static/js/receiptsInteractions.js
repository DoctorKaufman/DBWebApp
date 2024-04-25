document.addEventListener('alpine:init', () => {
    Alpine.data('receiptsInteractions', (activeTab, receipts, user) => ({
        activeTab: activeTab,
        receipts: receipts,
        user: user,

        init() {
            this.$watch('Alpine.store("receiptsState").receipts', value => {
                this.receipts = value;
                console.log('Receipts:', this.receipts);
            });
        }
    }));
});