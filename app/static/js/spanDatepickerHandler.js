document.addEventListener('alpine:init', () => {
    Alpine.data('spanDatepicker', () => ({
        from: '',
        to: '',

        init() {
            console.log("Range picker initialized")
            this.$watch('from', value => {
                console.log('From:', value);
            });
            this.$watch('to', value => {
                console.log('To:', value);
            });
        }
    }));
})