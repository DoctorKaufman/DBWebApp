document.addEventListener('alpine:init', () => {
    Alpine.store('receiptsState', {

        receiptsState: null,
        receiptSales: [],
        currentSale: null,
        dropdownOptions: [],
        maxAmount: 0,
    });
});