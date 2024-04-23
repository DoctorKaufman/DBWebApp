document.addEventListener('alpine:init', () => {
    Alpine.data('cardsInteractions', (currentTab, people, columns, keyColumn) => ({
        // #region initializations
        people: people,
        workersState: null,
        rawColumns: columns,
        fields: Object.entries(columns).map(([key, value]) => ({ [key]: value })),
        key_column: keyColumn,
        addingCard: false,

        init() {
            this.$store.workersState.currentTab = currentTab;
            this.$store.workersState.initializeElements(people);
            this.$store.workersState.columns = this.rawColumns;
            this.$store.workersState.fields = this.fields;
            this.$store.workersState.keyColumn = keyColumn;
            this.$store.currentFilters = {
                searchColumn: null,
                searchValue: null,
            },

            this.workersState = this.$store.workersState.globalState;

            this.$watch('Alpine.store("workersState").globalState', (newState) => {
                this.workersState = newState;

                console.log('Global state changed to:', this.workersState);
            });
        },
        // #endregion

        createNewCard() {
            Alpine.store('workersState').globalState = GlobalStates.ADDING;
            this.addingCard = true;
        },

    }));
});