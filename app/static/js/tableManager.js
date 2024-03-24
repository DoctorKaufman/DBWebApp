document.addEventListener('alpine:init', () => {
    Alpine.data('tableManager', () => ({
        
        currentlyEditingRowId: null, // ID of the currently editing row

        isRowEditable(rowId) {
            return this.currentlyEditingRowId === null || this.currentlyEditingRowId === rowId;
        },

        toggleRowEdit(rowId) {
            if (this.currentlyEditingRowId === null) {
                this.currentlyEditingRowId = rowId;
            } else if (this.currentlyEditingRowId === rowId) {
                this.currentlyEditingRowId = null; // Finish editing the current row
            } else {
                // Optionally show an error message that another row is currently being edited
                console.log("Another row is currently being edited.");
            }
        },

        saveEditedRow(rowId) {
            // Logic to save the edited row
            console.log(`Row ${rowId} saved.`);
            this.currentlyEditingRowId = null; // Reset after saving
        },

        // Add your other functions here...
    }));
});
