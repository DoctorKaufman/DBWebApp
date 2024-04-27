import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.data('dropdownGoodsSearch', () => ({
      isOpen: false,
      searchTerm: '',
      selectedOption: null,
      options: null,

      async init() {
        await this.prepareGoods();
      },

      toggleDropdown() {
        this.isOpen = !this.isOpen;
      },

      selectOption(option) {
        this.selectedOption = option;
        this.isOpen = false;
        this.$dispatch('input', option); 

        Alpine.store('receiptsState').currentSale = option;
        Alpine.store('receiptsState').maxAmount = option['Amount'];
        Alpine.store('receiptsState').currentSale['Amount'] = 0;
      },

      filteredOptions() {
        if (!this.options) return [];
        let filtered =  this.options.filter(option => {
            const name = option['Product_Name'] || '';
            return name.toLowerCase().includes(this.searchTerm.toLowerCase());
        });
        let result = (filtered.map(option => {
            return {
                Name: option.Product_Name,
                Price: option.Price,
                UPC: option.UPC,
                Amount: option.Amount,
            };
        }));
        console.log('Filtered:', result);
        return result;
      },

      async prepareGoods(){
        await sendRequest({
            action: 'get',
            currentPage: 'goods_in_store'
        })
            .then(response => {
                this.options = response;
            })
            .catch(error => {
                console.error('Error fetching goods from store:', error);
                createToast('error', `Error fetching goods from store: ${error}`);
            });
    },
    }));
  });
  