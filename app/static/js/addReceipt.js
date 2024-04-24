document.addEventListener('alpine:init', () => {
    Alpine.data('addReceipt', (user) => ({
        currentDate: new Date().toLocaleString(),
        user: null,
        storeProducts: [],
        dropdownOptions: [],

        init(){
            this.user = user;
            
        },

        addSale(){
            const addButton = document.getElementById('add-sale-button');

            sendRequest({
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
                    'Name' : product['Name']
                }
            });
        
            

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