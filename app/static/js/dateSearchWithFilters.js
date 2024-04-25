import { createToast, removeToast } from './toastNotifications.js';
import { sendRequest } from "./sendRequest.js";

document.addEventListener('alpine:init', () => {
    Alpine.data('dateSearchWithFilters', () => ({
        showDropdown: false,
        searchTerm: '',
        mapper: 'Search by',
        selectedOption: null,
        options: null,
        storeName: null,

        init(){
            this.options = [{'Cashier Surname (sum)' : 'sum'}, {'Cashier Surname (checks)' : 'statistic'}, {'Product Name' : 'product'}];
            this.storeName = 'receiptsState';
        },
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

            Alpine.store(this.storeName).currentFilters.searchColumn = dropdownValue;
            Alpine.store(this.storeName).currentFilters.searchValue = textSearchValue;

            const fromDate = encodeURIComponent(document.getElementById('dateFrom').value);
            const toDate = encodeURIComponent(document.getElementById('dateTo').value);
            console.log(fromDate, toDate);

            let url = `${baseUrl}/receipt/${dropdownValue}?start-date=${fromDate}&end-date=${toDate}`;

            if (textSearchValue){
                url += `&value=${textSearchValue}`;
            }

            console.log('URL:', url);

            axios.get(url)
                .then(response => {
                    console.log('Search successful:', response);
                    createToast('success', `Search for input ${this.selectedOption}: ${this.searchTerm} was successful.`);
                    console.log('Response data:', response.data);
                })
                .catch(error => {
                    console.error('Search error:', error);
                    createToast('error', `Search for input ${this.selectedOption}: ${this.searchTerm} failed.`);
                });
        }
    }));
  });
  