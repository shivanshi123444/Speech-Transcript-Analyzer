document.addEventListener('DOMContentLoaded', () => {
    const transcriptFileInput = document.getElementById('transcriptFile');
    const analyzeButton = document.getElementById('analyzeButton');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const summaryContent = document.getElementById('summaryContent');
    const actionItemsList = document.getElementById('actionItemsList');
    const insightsList = document.getElementById('insightsList');
    const attributedStatementsList = document.getElementById('attributedStatementsList');
    const attributedActionItemsInsights = document.getElementById('attributedActionItemsInsights');
    const errorDiv = document.getElementById('error');
    const errorMessage = document.getElementById('errorMessage');
    const exportPdfButton = document.getElementById('exportPdfButton');
    const exportCsvButton = document.getElementById('exportCsvButton');

    const API_BASE_URL = 'http://127.0.0.1:8000'; // Adjust if your backend runs on a different port/host

    analyzeButton.addEventListener('click', async () => {
        const file = transcriptFileInput.files[0];
        if (!file) {
            alert('Please select a transcript file.');
            return;
        }

        loadingDiv.classList.remove('hidden');
        resultsDiv.classList.add('hidden');
        errorDiv.classList.add('hidden');
        errorMessage.textContent = '';

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${API_BASE_URL}/analyze_transcript/`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Analysis failed.');
            }

            const data = await response.json();
            displayResults(data);
        } catch (err) {
            errorMessage.textContent = `Error: ${err.message}`;
            errorDiv.classList.remove('hidden');
            console.error('Error during analysis:', err);
        } finally {
            loadingDiv.classList.add('hidden');
        }
    });

    function displayResults(data) {
        summaryContent.textContent = data.summary;

        actionItemsList.innerHTML = '';
        if (data.action_items && data.action_items.length > 0) {
            data.action_items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `${item.item} (Responsible: ${item.responsible_party}, Deadline: ${item.deadline})`;
                actionItemsList.appendChild(li);
            });
        } else {
            actionItemsList.innerHTML = '<li>No action items identified.</li>';
        }

        insightsList.innerHTML = '';
        if (data.insights && data.insights.length > 0) {
            data.insights.forEach(insight => {
                const li = document.createElement('li');
                li.textContent = insight;
                insightsList.appendChild(li);
            });
        } else {
            insightsList.innerHTML = '<li>No key insights identified.</li>';
        }

        attributedStatementsList.innerHTML = '';
        if (data.attributed_statements && data.attributed_statements.length > 0) {
            const ul = document.createElement('ul');
            data.attributed_statements.forEach(statement => {
                const li = document.createElement('li');
                li.innerHTML = `<strong>${statement.speaker}:</strong> ${statement.statement}`;
                ul.appendChild(li);
            });
            attributedStatementsList.appendChild(ul);
        } else {
            attributedStatementsList.innerHTML = '<p>No speaker attributed statements found (check transcript format).</p>';
        }

        attributedActionItemsInsights.innerHTML = '';
        if (data.attributed_action_items_insights) {
            for (const speaker in data.attributed_action_items_insights.action_items) {
                const speakerDiv = document.createElement('div');
                speakerDiv.innerHTML = `<h4>${speaker}'s Action Items:</h4>`;
                const ul = document.createElement('ul');
                data.attributed_action_items_insights.action_items[speaker].forEach(item => {
                    const li = document.createElement('li');
                    li.textContent = `${item.item} (Responsible: ${item.responsible_party}, Deadline: ${item.deadline})`;
                    ul.appendChild(li);
                });
                speakerDiv.appendChild(ul);
                attributedActionItemsInsights.appendChild(speakerDiv);
            }

            for (const speaker in data.attributed_action_items_insights.insights) {
                const speakerDiv = document.createElement('div');
                speakerDiv.innerHTML = `<h4>${speaker}'s Insights:</h4>`;
                const ul = document.createElement('ul');
                data.attributed_action_items_insights.insights[speaker].forEach(insight => {
                    const li = document.createElement('li');
                    li.textContent = insight;
                    ul.appendChild(li);
                });
                speakerDiv.appendChild(ul);
                attributedActionItemsInsights.appendChild(speakerDiv);
            }

            if (Object.keys(data.attributed_action_items_insights.action_items).length === 0 &&
                Object.keys(data.attributed_action_items_insights.insights).length === 0) {
                attributedActionItemsInsights.innerHTML = '<p>No speaker-attributed action items or insights found.</p>';
            }

        } else {
            attributedActionItemsInsights.innerHTML = '<p>No speaker-attributed action items or insights found.</p>';
        }

        resultsDiv.classList.remove('hidden');
    }

    // Dummy export functionality (as explained in backend)
    exportPdfButton.addEventListener('click', () => {
        window.open(`${API_BASE_URL}/export_results/pdf/dummy-analysis-id`, '_blank');
    });

    exportCsvButton.addEventListener('click', () => {
        window.open(`${API_BASE_URL}/export_results/csv/dummy-analysis-id`, '_blank');
    });
});