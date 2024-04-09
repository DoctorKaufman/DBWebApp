function dropdownComponent() {
    return {
      isOpen: false,
      search: '',
      selected: 'Open Dropdown', // Initial text
      options: [], // Will be populated when component is initialized
      filteredOptions: [],
  
      init() {
        // Initialize filteredOptions with all options
        this.filteredOptions = this.options;
      },
  
      filterOptions() {
        this.filteredOptions = this.options.filter((option) =>
          option.toLowerCase().includes(this.search.toLowerCase())
        );
      },
  
      selectOption(option) {
        this.selected = option;
        this.isOpen = false;
      },
    };
  }
  
  document.addEventListener('alpine:init', () => {
    Alpine.data('dropdownComponent', dropdownComponent);
  });
  