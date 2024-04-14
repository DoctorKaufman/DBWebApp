import { createToast, removeToast } from './toastNotifications.js';
import { sendRequest } from "./sendRequest.js";

document.addEventListener('alpine:init', () => {
    Alpine.data('defaultSearch', (currentPage) => ({

        searchTerm: '',
        search() {
            const baseUrl = "http://127.0.0.1:5000"; // Replace with actual base URL
            const textSearchValue = encodeURIComponent(this.searchTerm);
            
            // Assuming 'Name' is always the search column
            const searchColumn = 'Name';
            
            Alpine.store('tableState').currentFilters.searchValue = textSearchValue;
            Alpine.store('tableState').currentFilters.searchColumn = searchColumn;
            
            // Perform the search request
            sendRequest({
                action: 'get',
                currentPage: currentPage, 
                searchColumn: searchColumn,
                searchValue: textSearchValue
            })
            .then(response => {
                console.log('Search successful:', response);
                Alpine.store('tableState').initializeRows(response);
                createToast('success', `Search for input ${searchColumn}: ${this.searchTerm} was successful.`);
            })
            .catch(error => {
                console.error('Search error:', error);
                createToast('error', `Search for input ${searchColumn}: ${this.searchTerm} failed.`);
            });
        }
    }));
});
