
document.addEventListener('alpine:init', () => {
    Alpine.data('requests',(active_tab) => ({
        activeTab: active_tab,
        value: '',
        result: null,
        query: 0,

        init() {
            this.query = this.activeTab === 'request1' ? 1 : 2;
            if (this.query === 2)
                this.sendRequest();
        },

        sendRequest() {
            let baseUrl = window.location.origin;
            axios.get(`${baseUrl}/query/${this.query}?${this.value ? `value=${this.value}` : ''}`)
                .then(response => {
                    console.log('Data fetched:', response.data);
                    this.result = response.data;
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    createToast('error', `Error fetching data: ${error}`);
                });
        }
    }));
});