import { sendRequest } from "./sendRequest.js";
import { createToast, removeToast } from './toastNotifications.js';

document.addEventListener('alpine:init', () => {
    Alpine.data('addReceipt', (user) => ({
        currentDate: new Date().toLocaleString(),
        user: null,
        customerPercent: 0,
        customerDiscount: 0,
        totalPrice: 0,
        taxesSum: 0,

        init(){
            this.user = user;
            this.totalPrice = 0;
            this.customerDiscount = 0;
            this.taxesSum = 0;
            Alpine.store('receiptsState').receiptSales = [];
            Alpine.store('receiptsState').currentSale = null;
            Alpine.store('receiptsState').currentCustomer = null;
            Alpine.store('receiptsState').receiptsState = GlobalStates.NONE;

            this.$watch('Alpine.store("receiptsState").currentCustomer', (newCustomer) => {
                if (newCustomer !== null){
                    this.customerPercent = newCustomer['Percent'];
                    this.reEvaluateTotal();
                }
            });
        },

        async addSale(){
            Alpine.store('receiptsState').receiptsState = GlobalStates.ADDING;
            const salesList = document.getElementById('sales-list');
            const row = document.createElement("li"); 
            row.setAttribute('id', 'current-sale');
        
            let innerHTML = `
                    <div class="flex justify-between items-center">

                    <div x-data="dropdownGoodsSearch()">
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
                        class="absolute z-40 w-1/2 mt-2ring-1 ring-black ring-opacity-5 p-1 space-y-1 bg-white 
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
                                    <span class="text-sm" x-text="option['Name'] +' : $'+ parseFloat(option['Price'])"></span>
                                </a>
                            </template>
                        </div>
                        </div>
                    </div>
                    
                    <div x-data="numberSpinner()" class="relative flex items-center max-w-[11rem]">
                        <button @click.prevent="decreaseQuantity()" 
                        class="bg-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600 dark:border-gray-600 hover:bg-gray-200 border border-gray-300 
                        rounded-s-lg p-3 h-11 focus:ring-gray-100 dark:focus:ring-gray-700 focus:ring-2 focus:outline-none"
                        :class="{'pointer-events-none opacity-50' : currentQuantity == 0 || !Alpine.store('receiptsState').currentSale}">
                            <svg class="w-3 h-3 text-gray-900 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 18 2">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h16"/>
                            </svg>
                        </button>
                        <input type="text" x-model="currentQuantity" x-on:input="validateQuantity" x-on:blur="validateQuantity" 
                        class="bg-gray-50 border-x-0 border-gray-300 h-11 font-medium text-center text-gray-900 text-sm focus:ring-blue-500 focus:border-blue-500 block w-full pb-6 dark:bg-gray-700 
                        dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        :class="{'pointer-events-none opacity-50' : !Alpine.store('receiptsState').currentSale}"
                        placeholder="" required />
                        <div class="absolute bottom-1 start-1/2 -translate-x-1/2 rtl:translate-x-1/2 flex items-center text-xs text-gray-400 space-x-1 rtl:space-x-reverse">
                            <svg class="w-2.5 h-2.5 text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8v10a1 1 0 0 0 1 1h4v-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5h4a1 1 0 0 0 1-1V8M1 10l9-9 9 9"/>
                            </svg>
                            <span>Amount</span>
                        </div>
                        <button @click.prevent="increaseQuantity()" 
                        class="bg-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600 dark:border-gray-600 hover:bg-gray-200 border border-gray-300 
                        rounded-e-lg p-3 h-11 focus:ring-gray-100 dark:focus:ring-gray-700 focus:ring-2 focus:outline-none"
                        :class="{'pointer-events-none opacity-50' : currentQuantity == max || !Alpine.store('receiptsState').currentSale}">
                            <svg class="w-3 h-3 text-gray-900 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 18 18">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 1v16M1 9h16"/>
                            </svg>
                        </button>
                    </div>

                    <div class="gap-5">
                        <button @click.prevent="cancelSale" class="text-white bg-red-700 hover:bg-red-800 focus:ring-4 aspect-square focus:outline-none focus:ring-red-300 font-medium rounded-full text-sm p-2.5 text-center inline-flex items-center me-2 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-800">
                        <i class="fa-solid fa-ban"></i>
                        </button>

                        <button @click.prevent="saveSale" class="text-white bg-cyan-700 hover:bg-cyan-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-full text-sm p-2.5 text-center inline-flex items-center me-2 dark:bg-cyan-600 dark:hover:bg-cyan-700 dark:focus:ring-blue-800">
                        <i class="fa-solid fa-arrow-right"></i>
                        </button>
                    </div>

                    </div>
            `;
            row.innerHTML = innerHTML;
            const lastElement = salesList.lastElementChild;
            salesList.insertBefore(row, lastElement);
        },

        cancelSale(){
            const currentSale = document.getElementById('current-sale');
            currentSale.remove();
            Alpine.store('receiptsState').receiptsState = GlobalStates.NONE;
        },

        saveSale(){
            console.log("Current sale: ", Alpine.store('receiptsState').currentSale);
            
            if(Alpine.store('receiptsState').currentSale === null){
                createToast('error', 'Please select a product before saving.');
                return;
            } else if ( Alpine.store('receiptsState').currentSale['Amount'] === 0){
                createToast('error', 'Please select a quantity greater than 0.');
                return;
            }
            Alpine.store('receiptsState').receiptSales.push(Alpine.store('receiptsState').currentSale);
            console.log("ALL Sales: ", Alpine.store('receiptsState').receiptSales);
            
            const sale = Alpine.store('receiptsState').currentSale;
            const salesList = document.getElementById('sales-list');
            const row = document.createElement("li"); 

            let innerHTML = `
            <div class="flex justify-between items-center">
                <span class="font-medium text-base">${sale.Name}</span>
                <span class="text-base font-medium">$${parseFloat(sale.Price)}</span>
            </div>
            <div class="flex justify-between items-center">
                <span>*Quantity:</span>
                <span>${sale.Amount} pieces</span>
            </div>
            `;

            row.innerHTML = innerHTML;
            
            this.totalPrice += parseFloat(sale.Price) * sale.Amount;
            this.customerDiscount = this.totalPrice * this.customerPercent / 100;
            this.customerDiscount = parseFloat(this.customerDiscount.toFixed(2));
            this.taxesSum = this.totalPrice * 0.2;
            this.taxesSum = parseFloat(this.taxesSum.toFixed(2));
            this.totalPrice += this.taxesSum;
            this.totalPrice -= this.customerDiscount;
            console.log("Total price: ", this.totalPrice);

            this.cancelSale();
            const lastElement = salesList.lastElementChild;
            salesList.insertBefore(row, lastElement);
        },

        cancelReceipt(){
            Alpine.store('receiptsState').receiptSales = [];
            Alpine.store('receiptsState').currentSale = null;
            Alpine.store('receiptsState').currentCustomer = null;
            this.totalPrice = 0;
            this.customerDiscount = 0;
            this.taxesSum = 0;
            this.customerPercent = 0;

            let list = document.getElementById('sales-list');
            while (list.firstChild && list.firstChild.id !== 'add-sale-button') {
                list.removeChild(list.firstChild);
            }

            createToast('success', 'Receipt canceled successfully.');
        },

        reEvaluateTotal(){
            this.totalPrice = 0;
            Alpine.store('receiptsState').receiptSales.forEach(sale => {
                this.totalPrice += parseFloat(sale.Price) * sale.Amount;
            });
            this.customerDiscount = this.totalPrice * this.customerPercent / 100;
            this.customerDiscount = parseFloat(this.customerDiscount.toFixed(2));
            this.taxesSum = this.totalPrice * 0.2;
            this.taxesSum = parseFloat(this.taxesSum.toFixed(2));
            this.totalPrice += this.taxesSum;
            this.totalPrice -= this.customerDiscount;
            console.log("Total price: ", this.totalPrice);
        },

        createReceipt(){
            console.log('Current customer:', Alpine.store('receiptsState').currentCustomer);
            let data = {
                "id_employee" : this.user['ID'],
                "card_number" : Alpine.store('receiptsState').currentCustomer? Alpine.store('receiptsState').currentCustomer['ID'] : null,
                "products" : Alpine.store('receiptsState').receiptSales.map(sale => {
                    return {
                        "upc" : sale['UPC'],
                        "amount" : sale['Amount'],
                        "price" : sale['Price']
                    };
                })
            }
            console.log("Receipt data: ", data);
            sendRequest({
                action: 'post',
                currentPage: 'receipts',
                data: data
            })
            .then(response => {
                console.log('Receipt created:', response);
                createToast('success', 'Receipt created successfully.');

                Alpine.store('receiptsState').refetchData();
                window.location.href = '/receipts';
            })
            .catch(error => {
                console.error('Error creating receipt:', error);
                createToast('error', 'Error creating receipt.');
            });
        },

    }));
});