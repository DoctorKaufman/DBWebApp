document.addEventListener('alpine:init', () => {
    Alpine.data('numberSpinner', (max) => ({
        currentQuantity: 0,
        max: max,

        increaseQuantity() {
            if (this.currentQuantity < max) {
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
            } else if (this.currentQuantity > max) {
                this.currentQuantity = max;
            }
        },

    }));
});