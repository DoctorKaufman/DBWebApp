document.addEventListener('alpine:init', () => {
    Alpine.data('rowComponent', (item) => ({
        editing: false,
        id: null,
        init() {
            activeTab = Alpine.store('tableState').currentTab;
            console.log(item)
            this.id = activeTab === 'goods_in_store' ? item['upc'] :
                      activeTab === 'goods' ? item['ID'] :
                      activeTab === 'categories' ? item['category_number'] : null;
        },

        toggleSelection() {
            this.$store.tableState.toggleItemSelection(this.id);
        },

        isChecked() {
            return this.$store.tableState.selectedItems.includes(this.id);
        },

        toggleRowEdit() {
            if (Alpine.store('tableState').globalState === GlobalStates.NONE) {
                this.originalValues = Array.from(document.querySelector('.table-body').querySelectorAll('input[type="text"]')).map(input => input.value);
                this.editing = true;
                Alpine.store('tableState').globalState = GlobalStates.EDITING;
            } else {
                createToast("error", "You can only fill information for one row at a time");
            }
        },

        saveEditedRow() {
            const parentElement = this.$el.parentNode.parentNode.parentNode;
            const inputs = parentElement.querySelectorAll('input[type="text"]');
            let allFilled = true;
        
            inputs.forEach(input => {
                if (input.value.trim() === '') {
                    allFilled = false;
                }
            });
        
            if (allFilled) {
                this.editing = false;
                Alpine.store('tableState').globalState = GlobalStates.NONE;
 
                const el = parentElement.querySelectorAll('.text-scramble');
                for (let i = 0; i < el.length; i++) {
                    const fx = new TextScramble(el[i])
                    fx.setText(inputs[i].value)
                }

                createToast("success", "Row saved successfully");
            } else {
                createToast("error", "Please fill in all fields before saving.");
            }
        },
        

        cancelEditingRow() {
            const inputs = document.querySelector('.table-body').querySelectorAll('input[type="text"]');
            inputs.forEach((input, index) => {
                input.value = this.originalValues[index] ?? ''; 
            });

            this.editing = false;
            Alpine.store('tableState').globalState = GlobalStates.NONE;
            createToast("info", "Editing cancelled");
        },
    }));

    class TextScramble {
      constructor(el) {
        this.el = el;
        this.update = this.update.bind(this);
        this.deleteText = this.deleteText.bind(this);
        this.typeText = this.typeText.bind(this);
      }
    
      setText(newText) {
        this.newText = newText;
        this.oldText = this.el.innerText;
        this.promise = new Promise((resolve) => this.resolve = resolve);
    
        this.deleteText();
        return this.promise;
      }
    
      deleteText() {
        const length = this.oldText.length;
        this.queue = [];
        for (let i = length; i >= 0; i--) {
          this.queue.push({ text: this.oldText.slice(0, i), start: (length - i) * 4, end: (length - i + 1) * 4 });
        }
        this.frame = 0;
        this.update(this.typeText);
      }
    
      typeText() {
        const length = this.newText.length;
        this.queue = [];
        for (let i = 0; i <= length; i++) {
          this.queue.push({ text: this.newText.slice(0, i), start: i * 4, end: (i + 1) * 4 });
        }
        this.frame = 0;
        this.update();
      }
    
      update(nextStep = null) {
        let output = '';
        let complete = 0;
        for (let i = 0, n = this.queue.length; i < n; i++) {
          let { text, start, end } = this.queue[i];
          if (this.frame >= end) {
            complete++;
            output = text;
          } else if (this.frame >= start) {
            output = text;
            break;
          }
        }
    
        this.el.innerHTML = output;
        if (complete === this.queue.length) {
          if (nextStep) {
            nextStep(); 
          } else {
            this.resolve();
          }
        } else {
          this.frameRequest = requestAnimationFrame(() => this.update(nextStep));
          this.frame++;
        }
      }
    }
    
    
});
