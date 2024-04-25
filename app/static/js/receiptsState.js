document.addEventListener('alpine:init', () => {
    Alpine.store('receiptsState', {

        receiptsState: null,
        receiptSales: [],
        dropdownOptions: [],
        maxAmount: 0,
    });
});