import { sendRequest } from './sendRequest.js';
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.data('tableInteractions', (currentTab, items, columns, keyColumn) => ({
        // #region initializations
        items: items,
        tableState: null,
        rawColumns: columns,
        fields: Object.entries(columns).map(([key, value]) => ({ [key]: value })),

        init() {
            this.$store.tableState.currentTab = currentTab;
            this.$store.tableState.initializeRows(items);
            this.$store.tableState.columns = this.rawColumns;
            this.$store.tableState.keyColumn = keyColumn;

            this.tableState = this.$store.tableState.globalState;

            this.$watch('Alpine.store("tableState").globalState', (newState) => {
                this.tableState = newState;

                console.log('Global state changed to:', this.tableState);
            });
        },
        // #endregion

        // #region row creation
        createRowForm() {
            const table = document.querySelector(".table-body");
            const row = document.createElement("tr"); 
            row.className = `bg-white border-b dark:bg-gray-800 dark:border-gray-700`; 
            row.id = 'row-creation-form';

            const fieldsJson = JSON.stringify(this.fields);
            row.setAttribute('x-data', `createRow(${fieldsJson})`);

            
            let innerHTML = '';

            this.fields.forEach(fieldObject => {
                const fieldName = Object.keys(fieldObject)[0]; 
                const inputRequired = fieldObject[fieldName];
        
                if (inputRequired) {
                    innerHTML += `<td class="px-6 py-4">
                                    <input type="text" id="${fieldName}"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 
                                    text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 
                                    block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 
                                    dark:placeholder-gray-400 dark:text-white 
                                    dark:focus:ring-cyan-500 dark:focus:border-cyan-500" 
                                    placeholder="${fieldName}"/>
                                </td>`;
                } else {
                    innerHTML += `<td class="px-6 py-4">
                                    <span>${fieldName} is autogenerated</span>
                                </td>`;
                }
            });

            innerHTML += `<td class="px-6 py-4 text-right max-w-16">
                            <div class="flex flex-row gap-4 justify-center">
                                <button @click="saveCreatedRow()" class="font-medium text-sky-600 dark:text-cyan-500 hover:underline">
                                    <span>Save</span>
                                </button>
                                <button @click="cancelCreatingRow()" class="font-medium text-red-600 dark:text-gray-400 hover:underline">
                                    <span>Cancel</span>
                                </button>
                            </div>
                        </td>`;

            row.innerHTML = innerHTML;

            const firstRow = table.firstChild;
            table.insertBefore(row, firstRow);
        },
        // #endregion

    }));
});