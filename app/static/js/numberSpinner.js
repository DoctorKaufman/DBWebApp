document.addEventListener('alpine:init', () => {
    Alpine.data('numberSpinner', () => ({
        currentQuantity: 0,
        max: Alpine.store('receiptsState').maxAmount,

        init(){
            this.currentQuantity = 0;
            this.max = Alpine.store('receiptsState').maxAmount;

            this.$watch('Alpine.store("receiptsState").maxAmount', (newAmount) => {
                this.max = newAmount;

                console.log('Max amount changed to:', this.max);
                if (this.currentQuantity > this.max) {
                    this.currentQuantity = this.max;
                }
            });
        },

        increaseQuantity() {
            if (this.currentQuantity < this.max) {
                this.currentQuantity++;
            }
        },

        decreaseQuantity() {
            if (this.currentQuantity > 0) {
                this.currentQuantity--;
            }
        },

        validateQuantity() {
            if (this.currentQuantity < 0) {
                this.currentQuantity = 0;
            } else if (this.currentQuantity > this.max) {
                this.currentQuantity = this.max;
            }
        },

    }));
});