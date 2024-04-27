import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.store('receiptsState', {

        receiptsState: null,
        receipts: [],
        receiptSales: [],
        currentSale: null,
        currentCustomer: null,
        selectedItems: [],
        maxAmount: 0,


        refetchData() {
            sendRequest({
                action: 'get', 
                currentPage: 'receipts', 
            })
                .then(response => {
                    console.log('Receipts fetched:', response);
                    this.receipts = response;
                    createToast("success", `Data refetched successfully`);
                })
                .catch(error => {
                    console.error('Error fetching receipts:', error);
                    createToast("error", "Error fetching receipts");
                });
        },

        startSelecting() {
            this.selectedItems = [];
            this.receiptsState = GlobalStates.SELECTING;
        },

        deleteSelected() {
            console.log('Removing items:', this.selectedItems);
            this.selectedItems.forEach(async itemId => {
                sendRequest({
                    action: 'delete', 
                    currentPage: 'receipts', 
                    id: itemId, 
                })
                    .then(response => {
                        console.log('Item deleted:', response);
                        createToast("success", "Receipt deleted successfully");
                        this.refetchData();
                    })
                    .catch(error => {
                        console.error('Error deleting item:', error);
                        createToast("error", `Error deleting receipt: ${itemId}`);
                    });
            });
            this.receiptsState = GlobalStates.NONE;
        },
    });
});