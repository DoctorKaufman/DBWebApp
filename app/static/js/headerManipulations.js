document.addEventListener('alpine:init', () => {

    Alpine.store('editingState', {
        globalEditingState: false,
    });

    Alpine.data('headerManipulations', () => ({
        
        selecting: false,
        selectedItems: [],
        selectAll: false,

        globalEditingState: false,
        // editing: false,

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

        rowComponent() {
            return {
                editing: false,
                id: null, // Initial state before setting the correct ID
                init(upc, ID, categoryId, activeTab) {
                    // Set the id based on active_tab's value
                    this.id = activeTab === 'goods_in_store' ? upc :
                              activeTab === 'goods' ? ID :
                              activeTab === 'categories' ? categoryId : null;
                    
                    console.log("Initialized row with ID:", this.id); // For debugging
                },

                toggleRowEdit() {
                    if (!Alpine.store('editingState').globalEditingState || this.editing) {
                        this.editing = !this.editing;
                        Alpine.store('editingState').globalEditingState = this.editing;
                    } else {
                        createToast("error", "You can only edit one row at a time");
                    }
                },

                saveEditedRow() {
                    this.editing = false;
                    Alpine.store('editingState').globalEditingState = false;
                    createToast("success", "Row saved successfully");
                }
            };
        },

        
    }));
});