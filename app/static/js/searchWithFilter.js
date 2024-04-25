import { createToast, removeToast } from './toastNotifications.js';
import { sendRequest } from "./sendRequest.js";

document.addEventListener('alpine:init', () => {
    Alpine.data('searchWithFilter', (currentPage) => ({
        showDropdown: false,
        searchTerm: '',
        mapper: 'Search by',
        selectedOption: null,
        options: null,
        storeName: null,

        init(){
            if (currentPage == 'goods'){
                this.options = [{'Name' : 'Name'}, {'Category' : 'Category'}];
                this.storeName = 'tableState';
            } else if (currentPage == 'goods_in_store'){
                this.options = [{'Promotional Product' : 'Promotional_Product'}, {'UPC' : 'upc'}];
                this.storeName = 'tableState';
            } else if (currentPage == 'workers'){
                this.options = [{'Surname' : 'Surname'}, {'Role' : 'Role'}];
                this.storeName = 'workersState';
            } else if (currentPage == 'clients'){
                this.options = [{'Surname' : 'Surname'}, {'Percent' : 'Percent'}];
                this.storeName = 'workersState';
            } else if (currentPage == 'receipts'){
                this.options = [{'Cashier Surname' : 'Surname'}, {'Product Name' : 'Product'}];
                this.storeName = 'receiptsState';
            }
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
            if (!this.selectedOption) {
                createToast('error', 'Please select a search option.');
                return;
            }
            const dropdownValue = encodeURIComponent(this.selectedOption);
            const textSearchValue = encodeURIComponent(this.searchTerm);

            Alpine.store(this.storeName).currentFilters.searchColumn = dropdownValue;
            Alpine.store(this.storeName).currentFilters.searchValue = textSearchValue;

            sendRequest({
                action: 'get',
                currentPage: currentPage,
                searchColumn: dropdownValue,
                searchValue: textSearchValue
            })
                .then(response => {
                    console.log('Search successful:', response);
                    createToast('success', `Search for input ${this.selectedOption}: ${this.searchTerm} was successful.`);
                    Alpine.store(this.storeName).initializeElements(response);
                })
                .catch(error => {
                    console.error('Search error:', error);
                    createToast('error', `Search for input ${this.selectedOption}: ${this.searchTerm} failed.`);
                });
        }
    }));
  });
  