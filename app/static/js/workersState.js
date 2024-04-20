import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';
import { TextScramble } from "./textScramble.js";

document.addEventListener('alpine:init', () => {    

    Alpine.store('workersState', {

        people: [],
        currentPerson: {},

        columns: {},
        keyColumn: null,
        fields: [],

        currentFilters: {
            searchColumn: null,
            searchValue: null,
        },
        sortState: {},

        currentTab: null,
        
        globalState: GlobalStates.NONE,

        selectedItems: [],
        selectAll: false,

        initializeCards(items) {
            this.people = items.map(item => ({
                ...item,
                editing: false, 
            }));
        },

        initializeCurrentElement(id = null) {
            const rowIndex = this.people.findIndex(element => element[this.keyColumn] === id);

            this.fields.forEach(fieldObject => {
                const fieldName = Object.keys(fieldObject)[0];
                if (fieldObject[fieldName] !== 'PK') {
                        if (rowIndex !== -1) {
                        this.currentPerson[fieldName] = this.people[rowIndex][fieldName];
                        } else {
                        this.currentPerson[fieldName] = '';
                        }
                    }
                });
            console.log('INITIALIZED ELEMENT: '+this.currentPerson);
        },

        editRow(id, newState) {
            if (this.globalState != GlobalStates.NONE) {
                createToast("error", `You can't edit another row while in ${this.globalState} mode.`);
            }
            else {
                this.initializeCurrentElement(id);
                const rowIndex = this.people.findIndex(element => element[this.keyColumn] === id);
                if (rowIndex !== -1) {
                    this.people[rowIndex].editing = newState;
                    this.globalState = GlobalStates.EDITING;
                }
            }
        },

        saveEditedRow(id) {
            const rowIndex = this.people.findIndex(element => element[this.keyColumn] == id);
            if (rowIndex !== -1) {
                this.fields.forEach(fieldObject => {
                    const fieldName = Object.keys(fieldObject)[0];
                    if (fieldObject[fieldName] === 'ATTRIB') {
                        this.currentPerson[fieldName] = document.getElementById(`${id}-${fieldName}-input`).value;
                    }
                });

                let element = this.currentPerson;
                console.log('Saving edited row:', element);
                sendRequest({
                    action: 'put',
                    currentPage: this.currentTab, 
                    id: id, 
                    data: this.currentPerson
                })
                    .then(response => {
                        createToast("success", "Item edited successfully");
                        const scrambleElementsArray = document.querySelector(`[data-key="${id}"]`).querySelectorAll('.text-scramble');
                        let scrambleElements = {};

                        scrambleElementsArray.forEach(element => {
                            const key = element.getAttribute('data-key');
                            scrambleElements[key] = element; 
                        });
                        for (let key in element) {
                            if (this.columns[key] === 'HIDDEN') 
                                continue;
                            const index = this.people[rowIndex][key];
                            if (String(index) != String(element[key])) {
                                this.people[rowIndex][key] = element[key];
                                const scramble = new TextScramble(scrambleElements[key]);
                                console.log("Current ELEMENT:", scrambleElements[key]);
                                console.log("Current NEW VALUE:", String(element[key]));
                                scramble.setText(String(element[key]));
                            }
                        }
                    })
                    .catch(error => {
                        console.error('Error editing item:', error);
                        createToast("error", `Error editing item`);
                    });
                this.currentPerson = {};
                this.people[rowIndex].editing = false;
                this.globalState = GlobalStates.NONE;
            }
        },

        cancelEditingRow(id){
            const rowIndex = this.people.findIndex(element => element[this.keyColumn] == id);
            if (rowIndex !== -1) {
                this.people[rowIndex].editing = false;
                this.globalState = GlobalStates.NONE;
            }
        },

        deleteCard(id) {
            sendRequest({
                action: 'delete', 
                currentPage: this.currentTab, 
                id: id, 
            })
                .then(response => {
                    console.log('Item deleted:', response);
                    createToast("success", "Item deleted successfully");
                    this.refetchData();
                })
                .catch(error => {
                    console.error('Error deleting item:', error);
                    createToast("error", `Error deleting item: ${id}`);
                });
        },

        deleteSelected() {
            const items = this.selectedItems;
            console.log('Removing items:', items);
            items.forEach(async itemId => {
                sendRequest({
                    action: 'delete', 
                    currentPage: this.currentTab, 
                    id: itemId, 
                })
                    .then(response => {
                        console.log('Item deleted:', response);
                        createToast("success", "Item deleted successfully");
                        this.refetchData();
                    })
                    .catch(error => {
                        console.error('Error deleting item:', error);
                        createToast("error", `Error deleting item: ${itemId}`);
                    });
            });
            this.stopSelecting();
        },

        toggleSelectAll() {
            this.selectAll = !this.selectAll;
            if (this.selectAll) {
                this.selectedItems = this.people.map(item => {
                    return item[this.keyColumn];
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

        refetchData(sortBy = null) {
            // Default sort order is ascending. Toggle the state if previously clicked.
            let sortOrder = 'asc';
            if (this.sortState[sortBy] && this.sortState[sortBy] === 'asc') {
                sortOrder = 'desc';
            } else {
                sortOrder = 'asc';
            }

            // Update the sortState with the new sortOrder
            this.sortState[sortBy] = sortOrder;

            sendRequest({
                action: 'get', 
                currentPage: this.currentTab, 
                sortBy: sortBy, 
                sortOrder: sortOrder,
                searchColumn: this.currentFilters.searchColumn,
                searchValue: this.currentFilters.searchValue
            })
                .then(response => {
                    console.log('Data fetched:', response);
                    this.initializeCards(response);
                    createToast("success", `Data sorted by ${sortBy} in ${sortOrder} order`);
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    createToast("error", "Error fetching data");
                });
        },
    });

});