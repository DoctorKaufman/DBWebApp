import { createToast, removeToast } from './toastNotifications.js';
import { sendRequest } from "./sendRequest.js";

document.addEventListener('alpine:init', () => {
    Alpine.data('searchWithFilter', (currentPage) => ({
        showDropdown: false,
        searchTerm: '',
        mapper: 'Search by',
        selectedOption: null,
        options: ['Name', 'Category'],

        toggleDropdown() {
            this.showDropdown = !this.showDropdown;
        },
        selectOption(option) {
            this.selectedOption = option;
            this.mapper = option;
            this.showDropdown = false;
        },
        search() {
            if (!this.selectedOption) {
                createToast('error', 'Please select a search option.');
                return;
            }
            const baseUrl = "http://127.0.0.1:5000"; // You'll need to replace this with your actual base URL
            const dropdownValue = encodeURIComponent(this.selectedOption);
            const textSearchValue = encodeURIComponent(this.searchTerm);

            Alpine.store('tableState').currentFilters.searchColumn = dropdownValue;
            Alpine.store('tableState').currentFilters.searchValue = textSearchValue;

            sendRequest({
                action: 'get',
                currentPage: currentPage,
                searchColumn: dropdownValue,
                searchValue: textSearchValue
            })
                .then(response => {
                    console.log('Search successful:', response);
                    createToast('success', `Search for input ${this.selectedOption}: ${this.searchTerm} was successful.`);
                    Alpine.store('tableState').initializeRows(response);
                })
                .catch(error => {
                    console.error('Search error:', error);
                    createToast('error', `Search for input ${this.selectedOption}: ${this.searchTerm} failed.`);
                });
        }
    }));
  });
  