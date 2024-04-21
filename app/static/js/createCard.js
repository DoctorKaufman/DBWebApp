import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.data('createCard', (fields) => ({

        currentTab: null,
        fillableFields: [],

        init() {
            this.currentTab = Alpine.store('workersState').currentTab;
            let parsedFields = JSON.stringify(fields);
            parsedFields = JSON.parse(parsedFields);
            this.fillableFields = parsedFields.reduce((acc, curr) => {
                const [key, value] = Object.entries(curr)[0];
                if (value === 'ATTRIB') {
                    acc.push(key);
                }
                return acc;
            }, []);
        },

        saveCreatedCard() {
            this.fillableFields.forEach(field => {
                if (field.toLowerCase().includes('date')) {
                    const dateString = document.getElementById(field).value;
                    Alpine.store('workersState').currentPerson[field] = this.reformatDateToDB(dateString);
                } else {
                    Alpine.store('workersState').currentPerson[field] = document.getElementById(field).value;
                }
            });

            const data = JSON.stringify(Alpine.store('workersState').currentPerson);
            console.log(data);

            let allFilled = true;
            for (let field in Alpine.store('workersState').currentPerson) {
                if (Alpine.store('workersState').currentPerson[field] === '') {
                    allFilled = false;
                    break;
                }
            }
        
            if (allFilled) {
                Alpine.store('workersState').globalState = GlobalStates.NONE;
                this.createRequest(data);
                this.selfDelete();
            } else {
                createToast("error", "Please fill in all fields before saving.");
            }
        },

        createRequest(data) {
            console.log("Data for request:", data);
            sendRequest({
                action: 'post',
                currentPage: this.currentTab,
                data: data
            })
                .then(response => {
                    createToast("success", "Card added successfully");
                    Alpine.store('workersState').refetchData();
                })
                .catch(error => {
                    createToast("error", error);
                });
            Alpine.store('workersState').currentPerson = {};
        },

        cancelCreatingCard() {

            Alpine.store('workersState').globalState = GlobalStates.NONE;
            createToast("info", "Adding of the item cancelled");
            this.selfDelete();
        },

        selfDelete(){
            document.getElementById('card-creation-form').remove();
        },

        reformatDateToDB(dateString) {
            const date = new Date(dateString);
            return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
        },
    }));
});
