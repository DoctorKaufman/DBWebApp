document.addEventListener('alpine:init', () => {
    Alpine.data('receiptsInteractions', (activeTab, receipts, user) => ({
        activeTab: activeTab,
        receipts: receipts,
        user: user,
        dateFrom: '',
        dateTo: '',

        init() {
            Alpine.store('receiptsState').receipts = receipts;

            this.$watch('dateFrom', value => {
                console.log('Date from:', value);
                Alpine.store('receiptsState').currentFilters.searchFrom = value;
            });
            this.$watch('dateTo', value => {
                console.log('Date to:', value);
                Alpine.store('receiptsState').currentFilters.searchTo = value;
            });
        }
    }));
});