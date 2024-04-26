import {sendRequest} from "./sendRequest";

document.addEventListener('alpine:init', () => {
    Alpine.data('request2',() => ({
        result: [],
        async init() {this.sendRequest()},

        async sendRequest() {
            let baseUrl = window.location.origin;
            //axios.get(`${baseUrl}/query/2`)
            axios.get(`http://127.0.0.1:5000/query/2`)
                .then(response => {
                    this.result = response;
                    console.log(this.result);
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    createToast('error', `Error fetching data: ${error}`);
                });
        }
    }));
});