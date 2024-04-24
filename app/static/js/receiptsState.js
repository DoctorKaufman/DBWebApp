document.addEventListener('alpine:init', () => {
    Alpine.store('receiptsState', {
        receiptSales: [],
    });
});