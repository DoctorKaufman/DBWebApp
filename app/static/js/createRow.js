document.addEventListener('alpine:init', () => {
    Alpine.data('createRow', () => ({

        activeTab: null,

        init() {
            this.activeTab = Alpine.store('tableState').currentTab;
            Alpine.store('tableState').globalState = GlobalStates.ADDING;
        },

        saveCreatedRow() {
            const inputs = document.querySelector('.table-body').querySelectorAll('input[type="text"]');
            let allFilled = true;
        
            inputs.forEach(input => {
                if (input.value.trim() === '') {
                    allFilled = false;
                }
                console.log(input.value);
            });
        
            if (allFilled) {
                Alpine.store('tableState').globalState = GlobalStates.NONE;
                createToast("success", "Row added successfully");
            } else {
                createToast("error", "Please fill in all fields before saving.");
            }
        },
        

        cancelCreatingRow() {

            Alpine.store('tableState').globalState = GlobalStates.NONE;
            createToast("info", "Adding of the item cancelled");

        },
    }));
});
