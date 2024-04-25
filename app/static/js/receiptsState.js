document.addEventListener('alpine:init', () => {
    Alpine.store('receiptsState', {

        receiptsState: null,
        receiptSales: [],
        currentSale: null,
        currentCustomer: null,
        maxAmount: 0,
    });
});