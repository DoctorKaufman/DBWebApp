import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.data('addReceipt', (user) => ({
        currentDate: new Date().toLocaleString(),
        user: null,
        storeProducts: [],
        dropdownOptions: [],

        init(){
            this.user = user;
            
        },

        async addSale(){
            const salesList = document.getElementById('sales-list');
            const row = document.createElement("li"); 
            // const addButton = document.getElementById('add-sale-button');

            await sendRequest({
                action: 'get',
                currentPage: 'goods_in_store'
            })
                .then(response => {
                    this.storeProducts = response;
                })
                .catch(error => {
                    console.error('Error fetching goods from store:', error);
                    createToast('error', `Error fetching goods from store: ${error}`);
                });
            
            this.dropdownOptions = this.storeProducts.map(product => {
                return {
                    'UPC' : product['UPC'],
                    'Price' : product['Price'],
                    'Name' : product['Product_Name']
                }
            });
            console.log("Passed to dropdown: ", this.dropdownOptions);
            Alpine.store('receiptsState').dropdownOptions = this.dropdownOptions;
        
            let innerHTML = `
                    <div class="flex justify-between items-center">

                    <div x-data="dropdownGoodsSearch()" class="relative group">
                        <button @click.prevent="toggleDropdown"
                        class="inline-flex justify-center w-full h-full text-sm font-medium text-gray-700 
                        bg-gray-50 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-blue-500 
                        focus:ring-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 
                        dark:placeholder-gray-400 dark:text-white dark:focus:ring-cyan-500 dark:focus:border-cyan-500">
                        <span x-text="selectedOption != null ? selectedOption['Name'] : 'Select product'"></span>
                        <svg class="w-5 h-5 ml-2 -mr-1" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M6.293 9.293a1 1 0 011.414 0L10 11.586l2.293-2.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
                        </svg>
                        </button>
                        <div x-show="isOpen" @click.away="isOpen = false" 
                        class="absolute right-0 mt-2ring-1 ring-black ring-opacity-5 p-1 space-y-1 z-10 bg-white 
                        divide-y divide-gray-100 dark:divide-gray-600 rounded-lg shadow dark:bg-gray-700 block">
                        <input x-model="searchTerm" class="bg-gray-50 border border-gray-300 text-gray-900 
                        text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 
                        dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white 
                        dark:focus:ring-cyan-500 dark:focus:border-cyan-500" placeholder="Search items" autocomplete="off">
                        <div class="overflow-auto max-h-40 custom-scrollbar">
                            <template x-for="option in filteredOptions()" :key="option['UPC']">
                                <a @click.prevent="selectOption(option)" href="javascript:void(0);" class="px-4 py-2 text-gray-700 dark:text-white 
                                cursor-pointer rounded-md inline-flex w-full hover:bg-gray-100 dark:hover:bg-gray-600 
                                dark:hover:text-white">
                                    <span x-text="option['Name'] +':'+ option['Price']"></span>
                                </a>
                            </template>
                        </div>
                        </div>
                    </div>
                        
                        <span class="text-base font-medium">$2.69</span>
                    </div>
            `;
            row.innerHTML = innerHTML;
            const lastElement = salesList.lastElementChild;
            salesList.insertBefore(row, lastElement);
        },

        createReceipt(){
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

    }));
});