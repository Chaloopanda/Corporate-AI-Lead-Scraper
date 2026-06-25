document.addEventListener('DOMContentLoaded', () => {
    const runBtn = document.getElementById('runBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const btnText = document.querySelector('.btn-text');
    const resultsSection = document.getElementById('resultsSection');
    const tableBody = document.getElementById('tableBody');
    const counter = document.getElementById('counter');
    const exportBtn = document.getElementById('exportBtn');

    let allResults = [];

    runBtn.addEventListener('click', async () => {
        // Reset UI
        allResults = [];
        tableBody.innerHTML = '';
        counter.textContent = '0';
        resultsSection.classList.remove('hidden');
        runBtn.disabled = true;
        btnText.textContent = 'Initializing Engine...';
        loadingSpinner.classList.remove('hidden');

        try {
            const response = await fetch('/api/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");
            let buffer = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const parts = buffer.split('\n\n');
                buffer = parts.pop(); // Keep the last incomplete part

                for (const part of parts) {
                    if (part.startsWith('data: ')) {
                        const jsonStr = part.replace('data: ', '');
                        const data = JSON.parse(jsonStr);
                        
                        if (data.status_msg) {
                            btnText.textContent = data.status_msg;
                            continue;
                        }
                        
                        allResults.push(data);
                        appendRow(data);
                        counter.textContent = allResults.length;
                    }
                }
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during scraping. Check console for details.');
        } finally {
            runBtn.disabled = false;
            btnText.textContent = 'Start Niche Discovery';
            loadingSpinner.classList.add('hidden');
        }
    });

    function appendRow(data) {
        const tr = document.createElement('tr');
        
        // Determine tier class for styling
        let tierClass = 'tier-cold';
        if (data['Lead Status'].includes('Tier 1')) tierClass = 'tier-1';
        else if (data['Lead Status'].includes('Tier 2')) tierClass = 'tier-2';

        tr.innerHTML = `
            <td><strong>${data.Name}</strong></td>
            <td>${data.Affiliation}</td>
            <td>${data.Email}</td>
            <td><span class="status ${tierClass}">${data['Lead Status']}</span></td>
            <td>${data['Work Model']}</td>
            <td><strong>${data['Internship Match']}</strong></td>
            <td>
                <div class="truncate" title="${data['Matched Paper/Project']}">
                    ${data['Matched Keyword'] !== 'None' ? `<strong>${data['Matched Keyword']}:</strong> ` : ''}
                    ${data['Matched Paper/Project']}
                </div>
            </td>
            <td><a href="${data['Profile Link']}" target="_blank">Profile ↗</a></td>
        `;
        tableBody.appendChild(tr);
    }

    exportBtn.addEventListener('click', () => {
        if (allResults.length === 0) {
            alert('No data to export.');
            return;
        }

        // Sort by score descending for export
        const sortedResults = [...allResults].sort((a, b) => b.Score - a.Score);

        // Generate Markdown table
        let markdown = '# Corporate & Remote AI Researcher Leads\n\n';
        markdown += '| Name | Affiliation | Email | Lead Status | Work Model | Internship | Matched Keyword | Profile Link |\n';
        markdown += '|---|---|---|---|---|---|---|---|\n';
        
        sortedResults.forEach(r => {
            markdown += `| ${r.Name} | ${r.Affiliation} | ${r.Email} | ${r['Lead Status']} | ${r['Work Model']} | ${r['Internship Match']} | ${r['Matched Keyword']} | [Link](${r['Profile Link']}) |\n`;
        });

        // Trigger download
        const blob = new Blob([markdown], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'corporate_remote_leads.md';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
});
