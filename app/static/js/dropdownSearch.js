document.addEventListener('alpine:init', () => {
    Alpine.data('dropdownComponent', (columnName) => ({
      isOpen: false,
      searchTerm: '',
      selectedOption: null,
      options: [],
      toggleDropdown() {
        this.isOpen = !this.isOpen;
      },
      selectOption(option) {
        this.selectedOption = option;
        this.isOpen = false;
        this.$dispatch('input', option); 

        Alpine.store('tableState').currentElement[columnName] = Object.keys(option)[0];
        console.log(Alpine.store('tableState').currentElement);
      },
      filteredOptions() {
        if (!this.options) return [];
        return this.options.filter((option) =>
          Object.values(option)[0].toLowerCase().includes(this.searchTerm.toLowerCase())
        );
      },
      init() {
        let request = ''
        if (columnName == "Category"){
            request = '/category/'
        } else if (columnName == "UPC Prom"){
            request = '/store-product/'
        } else if (columnName == "Product ID"){
            request = '/product/'
        }
        let url = `http://127.0.0.1:5000${request}droplist`;
        axios.get(url)
            .then(response => {
                console.log('GET request to', url, 'successful:', response.data);
                this.options = response.data;
            })
            .catch(error => {
                console.error('GET request to', url, 'failed:', error);
            });
        
        if (Alpine.store('tableState').currentElement[columnName] != null){
            this.selectedOption = {[Alpine.store('tableState').currentElement[columnName]]: Alpine.store('tableState').currentElement[columnName]};
        }
      }
    }));
  });
  