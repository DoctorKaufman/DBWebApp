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
        console.log( Alpine.store('receiptsState').receiptSales);
      },

      filteredOptions() {
        if (!this.options) return [];
        console.log('Search Term:', this.searchTerm);

        let filtered =  this.options.filter(option => {

            // Ensure option['Name'] is a string and is not undefined
            const name = option['Name'] || '';
            // console.log('Name:', name);
            console.log(name + 'inclueds' + this.searchTerm + '=' +name.toLowerCase().includes(this.searchTerm.toLowerCase()))
            return name.toLowerCase().includes(this.searchTerm.toLowerCase());
        });
        let result = (filtered.map(option => {
            return {
                Name: option.Name,
                Price: option.Price,
                UPC: option.UPC
            };
        }));
        console.log('Filtered:', result);
        return result;
      },
    }));
  });
  