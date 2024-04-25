document.addEventListener('alpine:init', () => {
    Alpine.data('dropdownGoodsSearch', () => ({
      isOpen: false,
      searchTerm: '',
      selectedOption: null,
      options: null,

      init() {
        this.options = Alpine.store('receiptsState').dropdownOptions;
      },

      toggleDropdown() {
        this.isOpen = !this.isOpen;
      },

      selectOption(option) {
        this.selectedOption = option;
        this.isOpen = false;
        this.$dispatch('input', option); 

        Alpine.store('receiptsState').receiptSales.push(option);
        Alpine.store('receiptsState').maxAmount = option['Amount'];
        console.log( Alpine.store('receiptsState').receiptSales);
      },

      filteredOptions() {
        if (!this.options) return [];
        console.log('Search Term:', this.searchTerm);

        let filtered =  this.options.filter(option => {
            const name = option['Name'] || '';
            return name.toLowerCase().includes(this.searchTerm.toLowerCase());
        });
        let result = (filtered.map(option => {
            return {
                Name: option.Name,
                Price: option.Price,
                UPC: option.UPC,
                Amount: option.Amount,
            };
        }));
        console.log('Filtered:', result);
        return result;
      },
    }));
  });
  