document.addEventListener('alpine:init', () => {
    Alpine.data('AddOrDeleteItem', () => ({

        selecting: false,
        selectedItems: [],
        selectAll: false,


        addCategory() {
            const data = { name: 'New Category Name', description: 'Description of the new category' };
            axios.post('http://127.0.0.1:5000/category/', data)
                .then(function (response) {
                    console.log('Category added successfully:' + response.data);
                    // Handle success, e.g., show a success message
                })
                .catch(function (error) {
                    console.error('Error adding category:', error);
                    // Handle error, e.g., showing an error message
                });
        },

        addProduct() {
            const data = {/* product data */};
            axios.post('http://127.0.0.1:5000/product/', data)
                .then(function (response) {
                    console.log('Product added successfully:' + response.data);
                    // Handle success
                })
                .catch(function (error) {
                    console.error('Error adding product:', error);
                    // Handle error
                });
        },

        removeCategory(event) {
            const categoryId = event.target.getAttribute('data-id');
            axios.delete(`http://127.0.0.1:5000/category/${categoryId}/`)
                .then(response => {
                // Handle the success case - maybe refresh the list of categories or give user feedback
                console.log('Category deleted:', response.data);
                })
                .catch(error => {
                // Handle the error case - show an error message to the user
                console.error('Error deleting category:', error);
                });
        },

        removeProduct(event) {
            const productId = event.target.getAttribute('data-id');
            axios.delete(`http://127.0.0.1:5000/product/${productId}/`)
                .then(response => {
                // Handle the success case - maybe refresh the list of categories or give user feedback
                console.log('Product deleted:', response.data);
                })
                .catch(error => {
                // Handle the error case - show an error message to the user
                console.error('Error deleting product:', error);
                });
        },

        init() {
            // Watch for changes on selectAll
            this.$watch('selectAll', (newVal) => {
                // Assuming items is the array that holds all the items in your table
                if (newVal) {
                    // If selectAll is true, add all the items to the selectedItems array
                    this.selectedItems = this.items.map(item => item.id); // Replace 'id' with the actual identifier of your items
                } else {
                    // If selectAll is false, clear the selectedItems array
                    this.selectedItems = [];
                }
            });
        },
    }));
});