import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.data('createRow', (fields) => ({

        currentTab: null,
        fillableFields: [],

        init() {
            Alpine.store('tableState').globalState = GlobalStates.ADDING;
            this.currentTab = Alpine.store('tableState').currentTab;
            this.fillableFields = fields.reduce((acc, curr) => {
                const [key, value] = Object.entries(curr)[0];
                if (value === 'ATTRIB') {
                    acc.push(key);
                }
                return acc;
            }, []);
        },

        saveCreatedRow() {
            this.fillableFields.forEach(field => {
                Alpine.store('tableState').currentElement[field] = document.getElementById(field).value;
            });

            const data = JSON.stringify(Alpine.store('tableState').currentElement);
            console.log(data);

            let allFilled = true;
            for (let field in Alpine.store('tableState').currentElement) {
                if (Alpine.store('tableState').currentElement[field] === '') {
                    allFilled = false;
                    break;
                }
            }
        
            if (allFilled) {
                Alpine.store('tableState').globalState = GlobalStates.NONE;
                this.createRequest(data);
                this.selfDelete();
            } else {
                createToast("error", "Please fill in all fields before saving.");
            }
        },

        createRequest(data) {
            sendRequest('post', this.currentTab, null, data)
                .then(response => {
                    createToast("success", "Row added successfully");
                    Alpine.store('tableState').refetchData();
                })
                .catch(error => {
                    createToast("error", error);
                });
            Alpine.store('tableState').currentElement = {};
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
