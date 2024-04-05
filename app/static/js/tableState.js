document.addEventListener('alpine:init', () => {

    const GlobalStates = {
        NONE: 'NONE',
        EDITING: 'EDITING',
        SELECTING: 'SELECTING',
        ADDING: 'ADDING',
    };

    window.GlobalStates = GlobalStates;
    

    Alpine.store('tableState', {

        rowElements: [],
        keyColumn: null,

        currentTab: null,
        
        globalState: GlobalStates.NONE,

        selectedItems: [],
        selectAll: false,

        initializeRows(items) {
            this.rowElements = items.map(item => ({
                ...item,
                editing: false, // Additional state as needed
                // Other row-specific states
            }));
        },

        editRow(id, newState) {
            const rowIndex = this.rowElements.findIndex(element => element[this.keyColumn] === id);
            if (rowIndex !== -1) {
                this.rowElements[rowIndex].editing = newState;
                this.globalState = GlobalStates.EDITING;
                // Handle other state changes as necessary
            }
        },

        saveEditedRow(id) {
            const rowIndex = this.rowElements.findIndex(element => element[this.keyColumn] === id);
            if (rowIndex !== -1) {
                // axios.put(`http://
                this.rowElements[rowIndex].editing = false;
                this.globalState = GlobalStates.NONE;
            }
        },

        cancelEditingRow(id){
            const rowIndex = this.rowElements.findIndex(element => element[this.keyColumn] === id);
            if (rowIndex !== -1) {
                this.rowElements[rowIndex].editing = false;
                this.globalState = GlobalStates.NONE;
            }
        },

        startSelecting() {
            this.globalState = GlobalStates.SELECTING;
        },

        stopSelecting() {
            this.globalState = GlobalStates.NONE;
            this.selectedItems = [];
            this.selectAll = false;
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
                        return item.category_number; // As per the given structure
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

});