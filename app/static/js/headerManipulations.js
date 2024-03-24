document.addEventListener('alpine:init', () => {

    Alpine.store('tableState', {
        globalEditingState: false,
        selecting: false,
        selectedItems: [],
        selectAll: false,
        toggleSelecting() {
            this.selecting = !this.selecting;
            if (this.selecting) {
                this.globalEditingState = false;
                document.dispatchEvent(new CustomEvent('exit-edit-mode'));
            }
        },
        toggleSelectAll(items, active_tab) {
            this.selectAll = !this.selectAll;
            if (this.selectAll) {
                this.selectedItems = items.map(item => {
                    if (active_tab === 'goods_in_store') {
                        return item.upc; // Assuming 'upc' exists for items in 'goods_in_store'
                    } else if (active_tab === 'goods') {
                        return item.ID; // Assuming 'ID' exists for items in 'goods'
                    } else if (active_tab === 'categories') {
                        return item.category_id; // As per the given structure
                    }
                });
            } else {
                this.selectedItems = [];
            }

            console.log("Selected items:", this.selectedItems);
        },
        toggleItemSelection(itemId) {
            const index = this.selectedItems.indexOf(itemId);
            if (index > -1) {
                this.selectedItems.splice(index, 1);
            } else {
                this.selectedItems.push(itemId);
            }
        },
        
        
    });

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

        removeCategory(event) {
            const categoryId = event.target.getAttribute('data-id');
            axios.delete(`http://127.0.0.1:5000/category/${categoryId}/`)
                .then(response => {
                    console.log('Category deleted:', response.data);
                })
                .catch(error => {
                    console.error('Error deleting category:', error);
                });
        },

        removeProduct(event) {
            const productId = event.target.getAttribute('data-id');
            axios.delete(`http://127.0.0.1:5000/product/${productId}/`)
                .then(response => {
                    console.log('Product deleted:', response.data);
                })
                .catch(error => {
                    console.error('Error deleting product:', error);
                });
        },

        rowComponent() {
            return {
                editing: false,
                id: null,
                init(upc, ID, categoryId, activeTab) {
                    this.id = activeTab === 'goods_in_store' ? upc :
                              activeTab === 'goods' ? ID :
                              activeTab === 'categories' ? categoryId : null;
                    
                    console.log("Initialized row with ID:", this.id); 

                    document.addEventListener('exit-edit-mode', () => {
                        if (this.editing) {
                            this.editing = false;
                        }
                    });
                },

                toggleSelection(){
                    this.$store.tableState.toggleItemSelection(this.id);
                },

                isChecked(){
                    return this.$store.tableState.selectedItems.includes(this.id);
                },

                toggleRowEdit() {
                    if (!Alpine.store('tableState').globalEditingState || this.editing) {
                        this.editing = !this.editing;
                        Alpine.store('tableState').globalEditingState = this.editing;
                    } else {
                        createToast("error", "You can only edit one row at a time");
                    }
                },

                saveEditedRow() {
                    this.editing = false;
                    Alpine.store('tableState').globalEditingState = false;
                    createToast("success", "Row saved successfully");
                },
            };
        },

        
    }));
});