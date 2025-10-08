class Modal {
    constructor(event, target, callback = null) {
        this.button = event;
        this.modal = target;
        this.initialize();
    }

    initialize() {
        const closeButtons = this.modal.querySelectorAll("button[name=close]");
        const saveButton = this.modal.querySelector("button[name=save]");

        // Helper to assist with event binding
        const on = (el, event, handler) => el?.addEventListener(event, handler);

        // Event to open the modal
        on(this.button, "click", this.open.bind(this));

        // Event to close the modal
        closeButtons.forEach(btn => on(btn, "click", this.close.bind(this)));

        // Event to close the modal by on the overlay
        // on(this.modal, "click", e => {
        //     if (e.target === this.modal) this.close();
        // });

        // Event to close with Escape Key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.classList.contains('active')) {
                this.close();
            }
        });

        // Confirm or save event
        on(saveButton, "click", () => this.save());
    }

    open() {
        this.modal.classList.add("active");
    }

    close() {
        this.modal.classList.remove("active")
    }
}