document.addEventListener('alpine:init', () => {
    Alpine.data('dropdownGoodsSearch', (options) => ({
      isOpen: false,
      searchTerm: '',
      selectedOption: null,
      options: options,

      init() {
        
      },

      toggleDropdown() {
        this.isOpen = !this.isOpen;
      },

      selectOption(option) {
        this.selectedOption = option;
        this.isOpen = false;
        this.$dispatch('input', option); 

        Alpine.store('receiptsState').receiptSales.push(option);
        console.log( Alpine.store('receiptsState').receiptSales);
      },

      filteredOptions() {
        if (!this.options) return [];
        return this.options.filter((option) =>
          option['Name'].toLowerCase().includes(this.searchTerm.toLowerCase())
        );
      },
    }));
  });
  