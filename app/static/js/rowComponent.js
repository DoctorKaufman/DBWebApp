document.addEventListener('alpine:init', () => {
    Alpine.data('rowComponent', (item) => ({
        editing: false,
        id: null,
        init() {
            activeTab = Alpine.store('tableState').currentTab;
            console.log(item)
            this.id = activeTab === 'goods_in_store' ? item['upc'] :
                      activeTab === 'goods' ? item['ID'] :
                      activeTab === 'categories' ? item['category_id'] : null;

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
