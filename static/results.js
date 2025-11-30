// Results page JavaScript for PitchGPT

let currentPrompt = '';

// Load and display results from sessionStorage
document.addEventListener('DOMContentLoaded', () => {
    const resultsData = sessionStorage.getItem('analysisResults');
    
    if (!resultsData) {
        // No results found, redirect back to home
        window.location.href = '/';
        return;
    }
    
    const data = JSON.parse(resultsData);
    
    // Display sources if available
    if (data.context) {
        displaySources(data.context);
    }
    
    // Store and show prompt button
    if (data.prompt) {
        currentPrompt = data.prompt;
        document.getElementById('promptButton').classList.remove('hidden');
    }
    
    // Render main analysis as Markdown
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = marked.parse(data.analysis);
    
    // Setup modal event listeners
    setupModals();
});

function setupModals() {
    const sourcesModal = document.getElementById('sourcesModal');
    sourcesModal.addEventListener('click', (e) => {
        if (e.target === sourcesModal) {
            closeSourcesModal();
        }
    });
    
    const promptModal = document.getElementById('promptModal');
    promptModal.addEventListener('click', (e) => {
        if (e.target === promptModal) {
            closePromptModal();
        }
    });
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeSourcesModal();
            closePromptModal();
        }
    });
}

function openSourcesModal() {
    const modal = document.getElementById('sourcesModal');
    modal.style.display = 'flex';
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeSourcesModal(event) {
    if (event) {
        event.stopPropagation();
    }
    const modal = document.getElementById('sourcesModal');
    modal.style.display = 'none';
    modal.classList.add('hidden');
    document.body.style.overflow = '';
}

function openPromptModal() {
    const modal = document.getElementById('promptModal');
    const promptText = document.getElementById('promptText');
    promptText.textContent = currentPrompt;
    modal.style.display = 'flex';
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closePromptModal(event) {
    if (event) {
        event.stopPropagation();
    }
    const modal = document.getElementById('promptModal');
    modal.style.display = 'none';
    modal.classList.add('hidden');
    document.body.style.overflow = '';
}

function displaySources(contextText) {
    const sourcesButton = document.getElementById('sourcesButton');
    const sourcesList = document.getElementById('sourcesList');
    
    if (!contextText || contextText.trim() === '' || contextText.includes('No retrieved context')) {
        sourcesButton.classList.add('hidden');
        return;
    }
    
    // Parse the context - format is:
    // - Source: filename (page X)
    //   - snippet 1
    //   - snippet 2
    const sourceBlocks = contextText.split(/^- Source:/im).filter(s => s.trim());
    
    if (sourceBlocks.length > 0) {
        sourcesButton.classList.remove('hidden');
        
        sourcesList.innerHTML = sourceBlocks.map(block => {
            const lines = block.trim().split('\n');
            let header = lines[0].trim();
            const snippets = lines.slice(1)
                .filter(l => l.trim().startsWith('-'))
                .map(l => l.replace(/^\s*-\s*/, '').trim());
            
            // Extract full path and clean filename
            // Format: "pitchgpt_rag/data/filename.pdf (page X)"
            const pathMatch = header.match(/(.+?)(?:\s*\(page\s+\d+\))?$/);
            if (pathMatch) {
                const fullPath = pathMatch[1].trim();
                const filename = fullPath.split('/').pop(); // Get just the filename
                const pageMatch = header.match(/\(page\s+(\d+)\)/i);
                const pageInfo = pageMatch ? ` (page ${pageMatch[1]})` : '';
                
                // Create download link - use /data endpoint
                const downloadPath = `/data/${filename}`;
                
                return `
                    <div class="source-card">
                        <div class="source-header">
                            <strong><a href="${downloadPath}" download="${filename}" class="pdf-title-link">${filename}${pageInfo}</a></strong>
                        </div>
                        ${snippets.length > 0 ? `
                            <div class="source-snippets">
                                ${snippets.map(s => `<p class="snippet">• ${s}</p>`).join('')}
                            </div>
                        ` : ''}
                    </div>
                `;
            }
            return '';
        }).join('');
    } else {
        sourcesButton.classList.add('hidden');
    }
}
