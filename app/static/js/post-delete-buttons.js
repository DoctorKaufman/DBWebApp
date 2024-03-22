document.addEventListener('alpine:init', () => {
    Alpine.data('AddOrDeleteItem', () => ({
        addCategory() {
            const data = { name: 'New Category Name', description: 'Description of the new category' };
            axios.post('http://127.0.0.1:5000/category/', data)
                .then(function (response) {
                    console.log('Category added successfully:', response.data);
                    // Handle success, e.g., showing a success message, or refreshing the category list
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
                    console.log('Product added successfully:', response.data);
                    // Handle success
                })
                .catch(function (error) {
                    console.error('Error adding product:', error);
                    // Handle error
                });
        },
    }));
});