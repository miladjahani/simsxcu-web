document.addEventListener('DOMContentLoaded', () => {
    const modeSelectors = document.querySelectorAll('input[name="mode"]');
    const designerForm = document.getElementById('designer-form');
    const metallurgistForm = document.getElementById('metallurgist-form');
    const solveButton = document.getElementById('solve-button');
    const resultsContainer = document.getElementById('results-container');
    const resultsOutput = document.getElementById('results-output');

    // --- Mode Switching Logic ---
    modeSelectors.forEach(selector => {
        selector.addEventListener('change', (event) => {
            const selectedMode = event.target.value;
            if (selectedMode === 'designer') {
                designerForm.classList.add('active');
                metallurgistForm.classList.remove('active');
            } else {
                designerForm.classList.remove('active');
                metallurgistForm.classList.add('active');
            }
        });
    });

    // --- Form Data Collection & API Call ---
    solveButton.addEventListener('click', async () => {
        const selectedMode = document.querySelector('input[name="mode"]:checked').value;
        const form = document.getElementById(`${selectedMode}-form`);
        const inputs = form.querySelectorAll('input');

        const params = {};
        inputs.forEach(input => {
            // Extract the key from the id (e.g., 'des_PLS_flow' -> 'PLS_flow')
            const key = input.id.split('_').slice(1).join('_');
            params[key] = parseFloat(input.value) || 0;
        });

        const requestBody = {
            mode: selectedMode,
            params: params
        };

        // --- UI Feedback & API Call ---
        solveButton.textContent = 'Solving...';
        solveButton.disabled = true;
        resultsContainer.classList.add('hidden');

        try {
            const response = await fetch('/api/v1/solve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            displayResults(data);

        } catch (error) {
            displayError(error);
        } finally {
            solveButton.textContent = 'Run Simulation';
            solveButton.disabled = false;
        }
    });

    // --- Result Display Functions ---
    function displayResults(data) {
        // Use JSON.stringify for a nicely formatted output
        resultsOutput.textContent = JSON.stringify(data, null, 4);
        resultsContainer.classList.remove('hidden');
    }

    function displayError(error) {
        resultsOutput.textContent = `An error occurred:\n\n${error.message}`;
        resultsContainer.classList.remove('hidden');
    }
});