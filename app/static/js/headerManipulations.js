document.addEventListener('alpine:init', () => {

    Alpine.data('headerManipulations', () => ({

        toggleSelecting() {
            this.$store.tableState.toggleSelecting();
        },
        
        addCategory() {
            const data = { name: 'New Category Name', description: 'Description of the new category' };
            axios.post('http://127.0.0.1:5000/category/', data)
                .then(response => {
                    console.log('Category added successfully:', response.data);
                    // Handle success, e.g., show a success message
                })
                .catch(error => {
                    console.error('Error adding category:', error);
                    // Handle error, e.g., showing an error message
                });
        },

        addProduct() {
            const data = {/* placeholder for product data */};
            axios.post('http://127.0.0.1:5000/product/', data)
                .then(response => {
                    console.log('Product added successfully:', response.data);
                    // Handle success
                })
                .catch(error => {
                    console.error('Error adding product:', error);
                    // Handle error
                });
        },

        removeCategory() {
            const categoryId = 'abc';//event.target.getAttribute('data-id');
            axios.delete(`http://127.0.0.1:5000/category/${categoryId}/`)
                .then(response => {
                    console.log('Category deleted:', response.data);
                })
                .catch(error => {
                    console.error('Error deleting category:', error);
                    createToast("error", `Error deleting category: ${categoryId}`);
                });
        },

        removeProduct() {
            const productId = 'abc'; //event.target.getAttribute('data-id');
            axios.delete(`http://127.0.0.1:5000/product/${productId}/`)
                .then(response => {
                    console.log('Product deleted:', response.data);
                })
                .catch(error => {
                    console.error('Error deleting product:', error);
                    createToast("error", `Error deleting product: ${productId}`);
                });
        },
    }));
});