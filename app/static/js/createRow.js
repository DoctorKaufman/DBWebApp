import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.data('createRow', (fields) => ({

        currentTab: null,
        fields: fields,

        init() {
            Alpine.store('tableState').globalState = GlobalStates.ADDING;
            this.currentTab = Alpine.store('tableState').currentTab;
            // this.fillableFields = fields.reduce((acc, curr) => {
            //     const [key, value] = Object.entries(curr)[0];
            //     if (value !== 'PK') {
            //         acc.push(key);
            //     }
            //     return acc;
            // }, []);
        },

        saveCreatedRow() {
            // const inputs = document.querySelector('.table-body').querySelectorAll('input[type="text"]');
            let allFilled = true;

            this.fields.forEach(fieldObject => {
                const fieldName = Object.keys(fieldObject)[0];

                if (fieldObject[fieldName] === 'FK') {
                    const dropdown = document.getElementById(`${fieldName}-creation-dropdown`);
                    if (dropdown.getAttribute(':id') === null) {
                        allFilled = false;
                    }
                } else if (fieldObject[fieldName] === 'ATTRIB') {
                    const input = document.getElementById(fieldName);
                    if (input.value === '') {
                        allFilled = false;
                    }
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

            this.fields.forEach(fieldObject => {
                const fieldName = Object.keys(fieldObject)[0];

                if (fieldObject[fieldName] === 'ATTRIB') {
                    data[fieldName] = document.getElementById(fieldName).value;
                } else if (fieldObject[fieldName] === 'FK') {
                    const dropdown = document.getElementById(`${fieldName}-creation-dropdown`);
                    data[fieldName] = parseInt(dropdown.getAttribute('id'));
                } else if (fieldObject[fieldName] === 'PK') {
                // Do nothing
                }
            });

            // console.log(data);
            // sendRequest('post', this.currentTab, null, data)
            //     .then(response => {
            //         // Handle success, e.g., show a success message
            //         createToast("success", "Row added successfully");
            //         Alpine.store('tableState').refetchData();
            //         // setTimeout(() => window.location.reload(), 800);
            //     })
            //     .catch(error => {
            //         // Handle error, e.g., showing an error message
            //         createToast("error", error);
            //     });
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
