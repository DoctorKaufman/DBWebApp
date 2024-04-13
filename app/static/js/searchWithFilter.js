import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.data('searchWithFilter', () => ({
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
            if (!this.selectedOption || !this.searchTerm) {
                alert('Please select a search option and enter a search term.');
                return;
            }
            const baseUrl = "http://127.0.0.1:5000"; // You'll need to replace this with your actual base URL
            const dropdownValue = encodeURIComponent(this.selectedOption);
            const textSearchValue = encodeURIComponent(this.searchTerm);
            const url = `${baseUrl}/product?sort=ID&order=desc&search-column=${dropdownValue}&search-value=${textSearchValue}`;

            console.log('Search URL:', url);
            axios.get(url)
                .then(response => {
                    console.log('Search successful:', response.data);
                    createToast('success', `Search for input ${this.selectedOption}: ${this.searchTerm} was successful.`);
                    Alpine.store('tableState').initializeRows(response.data);
                })
                .catch(error => {
                    console.error('Search error:', error);
                    createToast('error', `Search for input ${this.selectedOption}: ${this.searchTerm} failed.`);
                });
        }
    }));
  });
  