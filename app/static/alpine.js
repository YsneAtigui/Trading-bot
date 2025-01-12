document.addEventListener('alpine:init', () => {

    const socket = io();

    Alpine.data('app', () => ({
        strategy: 'sma',
        showModal: false,
        apiKey: localStorage.getItem('apiKey'),
        secretKey: localStorage.getItem('secretKey'),
        operations: [],

        init() {
            // Listen for 'update' events from the server
            console.log("init");
            
            socket.on('update', (data) => {
                console.log('Received update:', data);

                // Add the received data to the operations array
                this.operations.unshift(data);

                // Optional: Limit the size of the operations array
                if (this.operations.length > 100) {
                    this.operations.pop(); // Remove the oldest operation
                }
            });
        },

        switchStrategyType(type) {
            this.strategy = type
            this.formData.strategy_type = type
        },

        saveApiKeys() {
            localStorage.setItem('apiKey', this.formData.api_key);
            localStorage.setItem('secretKey', this.formData.secret_key);
            this.showModal = false;
            // alert('API Keys saved successfully!');
        },

        formData: {
            strategy_type: "sma",
            symbol: "",
            qty: "",
            sma_fast: "",
            sma_slow: "",
            api_key: localStorage.getItem('apiKey'),
            secret_key: localStorage.getItem('secretKey'),
        },
        responseData: null, // Store the API response
        error: null, // Store any errors

        async submitForm() {
            try {
                const response = await fetch('/strategy', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': "application/json"
                    },
                    body: JSON.stringify(this.formData)
                });

                if (!response.ok) {
                    console.log(response);
                    throw new Error(response.error);
                }

                const data = await response.json();
                this.responseData = data; // Store the response data
                this.error = null; // Clear any previous errors
            } catch (error) {
                this.error = error.message; // Store the error message
                this.responseData = null; // Clear any previous data
            }
        }
    }));


});