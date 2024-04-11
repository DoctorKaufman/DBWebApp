import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';
import { TextScramble } from "./textScramble.js";

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
        currentElement: {},

        columns: {},
        keyColumn: null,
        fields: [],

        currentTab: null,
        
        globalState: GlobalStates.NONE,
        sortState: {},

        selectedItems: [],
        selectAll: false,

        initializeRows(items) {
            this.rowElements = items.map(item => ({
                ...item,
                editing: false, 
            }));
        },

        initializeCurrentElement(id = null) {
            const rowIndex = this.rowElements.findIndex(element => element[this.keyColumn] === id);

            this.fields.forEach(fieldObject => {
                const fieldName = Object.keys(fieldObject)[0];
                if (fieldObject[fieldName] !== 'PK') {
                        if (rowIndex !== -1) {
                        this.currentElement[fieldName] = this.rowElements[rowIndex][fieldName];
                        } else {
                        this.currentElement[fieldName] = '';
                        }
                    }
                });
            console.log('INITIALIZED ELEMENT: '+this.currentElement);
        },

        editRow(id, newState) {
            if (this.globalState != GlobalStates.NONE) {
                createToast("error", `You can't edit another row while in ${this.globalState} mode.`);
            }
            else {
                this.initializeCurrentElement(id);
                const rowIndex = this.rowElements.findIndex(element => element[this.keyColumn] === id);
                if (rowIndex !== -1) {
                    this.rowElements[rowIndex].editing = newState;
                    this.globalState = GlobalStates.EDITING;
                }
            }
        },

        saveEditedRow(id) {
            const rowIndex = this.rowElements.findIndex(element => element[this.keyColumn] == id);
            if (rowIndex !== -1) {
                this.fields.forEach(fieldObject => {
                    const fieldName = Object.keys(fieldObject)[0];
                    if (fieldObject[fieldName] === 'ATTRIB') {
                        this.currentElement[fieldName] = document.getElementById(`${id}-${fieldName}-input`).value;
                    }
                });

                console.log("Current element sent for edit: "+Object.values(this.currentElement));
                let element = this.currentElement;
                sendRequest('put', this.currentTab, id, this.currentElement)
                    .then(response => {
                        createToast("success", "Item edited successfully");
                        const scrambleElementsArray = document.querySelector(`[data-key="${id}"]`).querySelectorAll('.text-scramble');
                        let scrambleElements = {};

                        scrambleElementsArray.forEach(element => {
                            const key = element.getAttribute('data-key');
                            scrambleElements[key] = element; 
                        });
                        for (let key in element) {
                            const index = this.rowElements[rowIndex][key];
                            if (index !== element[key]) {
                                this.rowElements[rowIndex][key] =element[key];
                                const scramble = new TextScramble(scrambleElements[key]);
                                console.log(scrambleElements[key]);
                                scramble.setText(element[key]);
                            }
                        }
                    })
                    .catch(error => {
                        console.error('Error editing item:', error);
                        createToast("error", `Error editing item`);
                    });
                this.currentElement = {};
                this.rowElements[rowIndex].editing = false;
                this.globalState = GlobalStates.NONE;
            }
        },

        cancelEditingRow(id){
            const rowIndex = this.rowElements.findIndex(element => element[this.keyColumn] == id);
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

        deleteSelected() {
            const items = this.selectedItems;
            console.log('Removing items:', items);
            items.forEach(async itemId => {
                await sendRequest('delete', this.currentTab, itemId, null)
                    .then(response => {
                        console.log('Item deleted:', response);
                        createToast("success", "Item deleted successfully");
                        // this.handleSuccessfullDeletion(itemId);  is it necessary??
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
                this.selectedItems = this.rowElements.map(item => {
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

        // handleSuccessfullDeletion(id){
        //     const rowIndex = this.rowElements.findIndex(element => element[this.keyColumn] == id);
        //     const selectedRowIndex = this.selectedItems.indexOf(id);
        //     if (rowIndex !== -1) {
        //         this.rowElements.splice(rowIndex, 1);
        //         this.selectedItems.splice(selectedRowIndex, 1);
        //     }
        // },

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

            sendRequest('get', this.currentTab, null, null, sortBy, sortOrder)
                .then(response => {
                    console.log('Data fetched:', response);
                    this.initializeRows(response);
                    createToast("success", `Data sorted by ${sortBy} in ${sortOrder} order`);
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    createToast("error", "Error fetching data");
                });
        },

        smartConvert(input) {
            if (!isNaN(input)) {
                // Convert to number if it's a valid number
                return Number(input);
            } else if (input.toLowerCase() === "true") {
                // Convert to boolean true
                return true;
            } else if (input.toLowerCase() === "false") {
                // Convert to boolean false
                return false;
            } else {
                // Return the original string if no conversion is possible
                return input;
            }
        },
    });

});