document.addEventListener('alpine:init', () => {
    Alpine.data('request2',() => ({
        result: [],
        init() {
            this.sendRequest()
        },

        sendRequest() {
            let baseUrl = window.location.origin;
            axios.get(`${baseUrl}/query/2`)
                .then(response => {
                    this.result = response.data;
                    console.log(this.result);
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    createToast('error', `Error fetching data: ${error}`);
                });
        }
    }));
});