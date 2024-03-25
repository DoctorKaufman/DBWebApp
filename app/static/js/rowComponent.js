document.addEventListener('alpine:init', () => {
    Alpine.data('rowComponent', () => ({
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

        toggleSelection() {
            this.$store.tableState.toggleItemSelection(this.id);
        },

        isChecked() {
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

        cancelEditingRow() {
            this.editing = false;
            Alpine.store('tableState').globalEditingState = false;
            createToast("info", "Editing cancelled");
        },
    }));
});
