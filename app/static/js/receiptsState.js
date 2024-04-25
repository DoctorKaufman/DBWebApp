document.addEventListener('alpine:init', () => {
    Alpine.store('receiptsState', {

        receiptsState: null,
        receipts: [],
        receiptSales: [],
        currentSale: null,
        currentCustomer: null,
        maxAmount: 0,


        // refetchData() {
        //     sendRequest({
        //         action: 'get', 
        //         currentPage: 'receipts', 
        //         // searchColumn: this.currentFilters.searchColumn,
        //         // searchValue: this.currentFilters.searchValue
        //     })
        //         .then(response => {
        //             console.log('Data fetched:', response);
        //             this.initializeElements(response);
        //             createToast("success", `Data sorted by ${sortBy} in ${sortOrder} order`);
        //         })
        //         .catch(error => {
        //             console.error('Error fetching data:', error);
        //             createToast("error", "Error fetching data");
        //         });
        // },
    });
});