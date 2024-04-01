document.addEventListener('alpine:init', () => {
    Alpine.data('createRow', () => ({

        currentTab: null,

        init() {
            Alpine.store('tableState').globalState = GlobalStates.ADDING;
            this.currentTab = Alpine.store('tableState').currentTab;
            console.log('Global state changed to:', this.$store.tableState.globalState);
        },

        saveCreatedRow() {
            const inputs = document.querySelector('.table-body').querySelectorAll('input[type="text"]');
            let allFilled = true;
        
            inputs.forEach(input => {
                if (input.value.trim() === '') {
                    allFilled = false;
                }
                console.log(input.value);
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
            const categoryName = document.querySelector('#category_name').value;
            const data = {
                "category_name": categoryName,
            };
            this.sendRequest('post', 'http://127.0.0.1:5000/category/', data)
                .then(data => {
                    // Handle success, e.g., show a success message
                    createToast("success", "Row added successfully");
                    setTimeout(() => window.location.reload(), 1000);
                })
                .catch(error => {
                    // Handle error, e.g., showing an error message
                    createToast("error", error);
                });
        },
        
        sendRequest(action, url, data = null) {
            // Configure the request options based on the action
            const options = {
                method: action,
                url: url,
            };
        
            // If the action requires data (e.g., POST), include it in the request
            if (['post', 'put', 'patch'].includes(action.toLowerCase()) && data) {
                options.data = data;
            }
        
            // Make the request using axios and return the Promise
            return axios(options)
                .then(response => {
                    console.log(`${action.toUpperCase()} request to ${url} successful:`, response.data);
                    return response.data; // Resolve the promise with the response data
                })
                .catch(error => {
                    console.error(`${action.toUpperCase()} request to ${url} failed:`, error);
                    throw error; // Reject the promise with the error
                });
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
