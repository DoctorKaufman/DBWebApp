document.addEventListener('alpine:init', () => {
  // Define the dropdown component
  Alpine.data('dropdownComponent', (options) => ({
      isOpen: false,
      searchTerm: '',
      selectedOption: null,
      options: options,
      toggleDropdown() {
        console.log('toggleDropdown');
          this.isOpen = !this.isOpen;
          console.log('this.isOpen:', this.isOpen);
      },
      selectOption(option) {
          this.selectedOption = option;
          this.isOpen = false;
          this.$dispatch('input', option); // Dispatch an event with the selected option
      },
      filteredOptions() {
          return this.options.filter((option) =>
              option.toLowerCase().includes(this.searchTerm.toLowerCase())
          );
      },
      init() {
          // Initialize the component (if any initial setup is required)
      }
  }));
});
