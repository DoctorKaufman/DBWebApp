import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.data('dropdownCustomerSearch', () => ({
      isOpen: false,
      searchTerm: '',
      selectedOption: null,
      options: null,

      async init() {
        await this.prepareCustomers();
      },

      toggleDropdown() {
        this.isOpen = !this.isOpen;
      },

      selectOption(option) {
        this.selectedOption = option;
        this.isOpen = false;
        this.$dispatch('input', option); 

        Alpine.store('receiptsState').currentCustomer = option;
      },

      filteredOptions() {
        if (!this.options) return [];
        console.log('Search Term:', this.searchTerm);

        let filtered =  this.options.filter(option => {
            const name = option['Name'] + option['Surname'] || '';
            return name.toLowerCase().includes(this.searchTerm.toLowerCase());
        });
        let result = (filtered.map(option => {
            return {
                ID: option.ID,
                Name: option.Name,
                Surname: option.Surname,
                Percent: option.Percent,
            };
        }));
        return result;
      },

      async prepareCustomers(){
        await sendRequest({
            action: 'get',
            currentPage: 'clients'
        })
            .then(response => {
                this.options = response;
                console.log('Customers fetched:', this.options);
            })
            .catch(error => {
                console.error('Error fetching customers:', error);
                createToast('error', `Error fetching customers: ${error}`);
            });
    }
    }));
  });
  