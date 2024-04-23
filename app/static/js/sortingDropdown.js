document.addEventListener('alpine:init', () => {
    Alpine.data('sortingDropdown', (currentPage, fields) => {
        return {

            showDropdown: false,
            selectedOption: null,
            options: null,
            mapper: 'Sort by',
            storeName: 'workersState',

            init() {
                console.log("fields: ", fields)
                this.options = fields.filter(field => Object.values(field)[0] !== 'HIDDEN')
            },
            toggleDropdown() {
                this.showDropdown = !this.showDropdown;
            },
            selectOption(option) {
                this.selectedOption = Object.keys(option)[0];
                this.mapper = "Sorting by " + Object.keys(option)[0];
                this.showDropdown = false;

                const dropdownValue = encodeURIComponent(this.selectedOption);

                // Alpine.store(this.storeName).currentFilters.sortBy = dropdownValue;
                console.log('Selected option:', this.selectedOption);
                console.log('Dropdown value:', dropdownValue);
                console.log('Current filters:', Alpine.store(this.storeName).currentFilters);
                Alpine.store(this.storeName).refetchData(dropdownValue);
            },
        };
    });
});