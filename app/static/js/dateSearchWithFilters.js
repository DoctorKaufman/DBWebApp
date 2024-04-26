import { createToast, removeToast } from './toastNotifications.js';
import { sendRequest } from "./sendRequest.js";

document.addEventListener('alpine:init', () => {
    Alpine.data('dateSearchWithFilters', () => ({
        showDropdown: false,
        searchTerm: '',
        mapper: 'Search by',
        selectedOption: null,
        options: [{'Cashier (sum)' : 'sum'}, {'Cashier (checks)' : 'statistic'}, {'Product Name' : 'product'}],
        storeName: 'receiptsState',

       
        toggleDropdown() {
            this.showDropdown = !this.showDropdown;
        },
        selectOption(option) {
            this.selectedOption = Object.values(option)[0];
            this.mapper = Object.keys(option)[0];
            this.showDropdown = false;
        },
        search() {
            const baseUrl = window.location.origin;

            if (!this.selectedOption) {
                createToast('error', 'Please select a search option.');
                return;
            }
            const dropdownValue = encodeURIComponent(this.selectedOption);
            const textSearchValue = encodeURIComponent(this.searchTerm);

            const fromDate = encodeURIComponent(document.getElementById('dateFrom').value);
            const toDate = encodeURIComponent(document.getElementById('dateTo').value);
            console.log(fromDate, toDate);

            if (!fromDate || !toDate) {
                createToast('error', 'Please select a date range.');
                return;
            }

            if (dropdownValue == 'product' && !textSearchValue) {
                createToast('error', 'Please enter a product name.');
                return;
            }

            let url = `${baseUrl}/receipt/${dropdownValue}?start-date=${fromDate}&end-date=${toDate}`;

            if (textSearchValue){
                url += `&value=${textSearchValue}`;
            }

            console.log('URL:', url);

            axios.get(url)
                .then(response => {
                    console.log('Search successful:', response);
                    console.log('Response data:', response.data);
                    if (this.selectedOption == 'statistic'){
                        Alpine.store(this.storeName).receipts = response.data;
                        createToast('success', `Search for input ${this.selectedOption}: ${this.searchTerm} was successful.`);
                    } else if (this.selectedOption == 'sum') {
                        let sum = Object.values(response.data)[0];
                        if (!sum) {
                            sum = 0;
                        }
                        createToast('success', `Sum of the sales = $${sum}`);
                    } else {
                        let amount = Object.values(response.data)[0];
                        if (!amount) {
                            amount = 0;
                        }
                        createToast('success', `Sales of ${this.searchTerm} = ${amount}`);
                    }
                })
                .catch(error => {
                    console.error('Search error:', error);
                    createToast('error', `Search for input ${this.selectedOption}: ${this.searchTerm} failed.`);
                });
        }
    }));
  });
  