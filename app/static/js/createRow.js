document.addEventListener('alpine:init', () => {
    Alpine.data('createRow', () => ({

        init() {
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
                this.selfDelete();
            } else {
                createToast("error", "Please fill in all fields before saving.");
            }
        },
        

        cancelCreatingRow() {

            Alpine.store('tableState').globalState = GlobalStates.NONE;
            createToast("info", "Adding of the item cancelled");
            this.selfDelete();
        },

        selfDelete(){
            document.getElementById('row-creation-form').remove();
        },
    }));
});
