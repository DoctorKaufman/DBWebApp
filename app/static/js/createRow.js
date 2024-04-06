import { sendRequest } from "./sendRequest.js";
import { createToast } from "./toastNotifications.js";

document.addEventListener('alpine:init', () => {
    Alpine.data('createRow', (fields) => ({

        currentTab: null,
        fillableFields: null,

        init() {
            Alpine.store('tableState').globalState = GlobalStates.ADDING;
            this.currentTab = Alpine.store('tableState').currentTab;
            this.fillableFields = fields.reduce((acc, curr) => {
                const [key, value] = Object.entries(curr)[0];
                if (value) {
                    acc.push(key);
                }
                return acc;
            }, []);
        },

        saveCreatedRow() {
            const inputs = document.querySelector('.table-body').querySelectorAll('input[type="text"]');
            let allFilled = true;
        
            inputs.forEach(input => {
                if (input.value.trim() === '') {
                    allFilled = false;
                }
            });
        
            if (allFilled) {
                Alpine.store('tableState').globalState = GlobalStates.NONE;
                this.createRequest();
                this.selfDelete();
            } else {
                createToast("error", "Please fill in all fields before saving.");
            }
        },

        createRequest() {
            let data = {};

            for (let i = 0; i < this.fillableFields.length; i++) {
                data[this.fillableFields[i]] = document.getElementById(this.fillableFields[i]).value;
            }
            console.log(data);
            sendRequest('post', this.currentTab, data)
                .then(response => {
                    // Handle success, e.g., show a success message
                    createToast("success", "Row added successfully");
                    setTimeout(() => window.location.reload(), 800);
                })
                .catch(error => {
                    // Handle error, e.g., showing an error message
                    createToast("error", error);
                });
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
