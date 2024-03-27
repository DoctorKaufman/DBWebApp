document.addEventListener('alpine:init', () => {

    Alpine.data('headerManipulations', (currentTab) => ({

        tableState: null,

        init() {
            this.$store.tableState.currentTab = currentTab;

            this.tableState = this.$store.tableState.globalState;

            this.$watch('Alpine.store("tableState").globalState', (newState) => {
                this.tableState = newState;

                console.log('Global state changed to:', newState);
            });
        },

        startSelecting() {
            this.$store.tableState.startSelecting();
            console.log(this.$store.tableState.globalState)
        },

        stopSelecting() {
            this.$store.tableState.stopSelecting();
        },
        
        addCategory() {
            const data = { name: 'New Category Name', description: 'Description of the new category' };
            axios.post('http://127.0.0.1:5000/category/', data)
                .then(response => {
                    console.log('Category added successfully:', response.data);
                    // Handle success, e.g., show a success message
                })
                .catch(error => {
                    console.error('Error adding category:', error);
                    // Handle error, e.g., showing an error message
                });

            newItem = this.createEmptyItem();
            this.createRow(newItem);
        },

        addProduct() {
            const data = {/* placeholder for product data */};
            axios.post('http://127.0.0.1:5000/product/', data)
                .then(response => {
                    console.log('Product added successfully:', response.data);
                    // Handle success
                })
                .catch(error => {
                    console.error('Error adding product:', error);
                    // Handle error
                });
        },

        createEmptyItem(){
            currentTab = this.$store.tableState.currentTab;

            if (currentTab === 'categories') {
                return { "name": '', "category_id": '#123456'};
            } else if (currentTab === 'goods') {
                return { "name": '', "ID": '#123456', "producer": '', "characteristics": ''};
            } else if (currentTab === 'goods_in_store') {
                return { "name": '', "upc": '#123456', "amount": '', "category": '', "price": ''};
            }
            return null;
        },

        createRow(item) {
            const table = document.querySelector(".table-body");
            const row = document.createElement("tr"); 
            row.className = `bg-white border-b dark:bg-gray-800 dark:border-gray-700`; 
            row.setAttribute('x-data', `rowComponent(${JSON.stringify(item)}, true)`);
            let innerHTML = `<td x-cloak x-show="tableState == GlobalStates.SELECTING" class="w-4 p-4">
                <div class="flex items-center">
                    <input type="checkbox" :checked="isChecked()" @change="toggleSelection()"
                        class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                    <label for="checkbox-table-search-1" class="sr-only">checkbox</label>
                </div>
            </td>`;

            Object.entries(item).forEach(([key, value]) => {
                if (key === 'name') {
                    innerHTML += `<th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                    <span x-show="!editing">${value}</span>
                                    <input x-cloak x-show="editing" type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" value="" />
                                </th>`;
                } else {
                    innerHTML += `<td class="px-6 py-4">
                                    <span x-show="!editing">${value}</span>
                                    <input x-cloak x-show="editing" type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" value="" />
                                </td>`;
                }
            });

            innerHTML += `<td x-show="tableState != GlobalStates.SELECTING" class="px-6 py-4 text-right max-w-16">
                            <button x-show="!editing" @click="toggleRowEdit()" class="font-medium text-sky-600 dark:text-blue-500 hover:underline">
                                <span>Edit</span>
                            </button>
                            <div x-show="editing" x-cloak class="flex flex-row gap-4 justify-center">
                                <button @click="saveEditedRow()" class="font-medium text-sky-600 dark:text-blue-500 hover:underline">
                                    <span>Save</span>
                                </button>
                                <button @click="cancelEditingRow()" class="font-medium text-red-600 dark:text-gray-400 hover:underline">
                                    <span>Cancel</span>
                                </button>
                            </div>
                        </td>`;

            row.innerHTML = innerHTML;

            const firstRow = table.firstChild;
            table.insertBefore(row, firstRow);
        },

        removeCategory() {
            const categoryId = 'abc';//event.target.getAttribute('data-id');
            axios.delete(`http://127.0.0.1:5000/category/${categoryId}/`)
                .then(response => {
                    console.log('Category deleted:', response.data);
                })
                .catch(error => {
                    console.error('Error deleting category:', error);
                    createToast("error", `Error deleting category: ${categoryId}`);
                });
        },

        removeProduct() {
            const productId = 'abc'; //event.target.getAttribute('data-id');
            axios.delete(`http://127.0.0.1:5000/product/${productId}/`)
                .then(response => {
                    console.log('Product deleted:', response.data);
                })
                .catch(error => {
                    console.error('Error deleting product:', error);
                    createToast("error", `Error deleting product: ${productId}`);
                });
        },
    }));
});