// Main page JavaScript for PitchGPT

// Prompt templates for preview
const promptTemplates = {
    'concise_analysis': `Analyze this startup pitch concisely. No explanations, just direct points.

**Risks:**
- [risk 1]
- [risk 2]

**Due Diligence Questions:**
- [question 1]
- [question 2]

Pitch:
{pitch_text}

Retrieved Context:
{context}`,
    'default_analysis': `Analyze this startup pitch and provide:
1. Two potential risks
2. Three follow-up questions for due diligence

Use the retrieved context to strengthen or challenge your reasoning.

Pitch:
{pitch_text}

Retrieved Context:
{context}

---
Format your response clearly:

**Risks:**
- ...
- ...

**Follow-up Questions:**
- ...
- ...
- ...`,
    'verbose_analysis': `Provide a comprehensive analysis of this startup pitch with detailed insights:

1. **Market Analysis** (3-4 paragraphs):
   - Assess the market opportunity and size
   - Evaluate competitive landscape
   - Identify market trends and dynamics

2. **Business Model Evaluation** (2-3 paragraphs):
   - Analyze revenue streams and unit economics
   - Assess scalability and sustainability
   - Evaluate competitive advantages

3. **Risk Assessment** (4-5 detailed risks):
   - Provide in-depth analysis of each risk
   - Include market, execution, financial, and competitive risks
   - Cite specific concerns from the pitch or retrieved context

4. **Due Diligence Questions** (5-7 questions):
   - Organize by category (financial, technical, team, market)
   - Provide context for why each question matters

5. **Investment Recommendation** (2 paragraphs):
   - Synthesize findings into clear recommendation
   - Highlight key factors influencing the decision

Use the retrieved context extensively to support your analysis with data and examples.

Pitch:
{pitch_text}

Retrieved Context:
{context}`
};

const promptTitles = {
    'concise_analysis': 'Quick Analysis - Prompt Template',
    'default_analysis': 'Standard Analysis - Prompt Template',
    'verbose_analysis': 'Deep Dive Analysis - Prompt Template'
};

function previewPrompt(promptKey, event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    
    const modal = document.getElementById('promptPreviewModal');
    const titleElement = document.getElementById('previewModalTitle');
    const textElement = document.getElementById('promptPreviewText');
    
    if (!modal || !titleElement || !textElement) {
        return;
    }
    
    titleElement.textContent = promptTitles[promptKey] || 'Prompt Template Preview';
    textElement.textContent = promptTemplates[promptKey] || 'Prompt template not found.';
    
    modal.classList.remove('hidden');
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closePromptPreviewModal() {
    const modal = document.getElementById('promptPreviewModal');
    modal.style.display = 'none';
    modal.classList.add('hidden');
    document.body.style.overflow = '';
}

async function analyzePitch() {
    const pitchText = document.getElementById('pitch').value.trim();
    
    if (!pitchText) {
        alert('Please enter a pitch deck to analyze');
        return;
    }

    const promptType = document.querySelector('input[name="analysisType"]:checked').value;
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loadingOverlay = document.getElementById('loadingOverlay');
    
    // Show loading overlay
    loadingOverlay.classList.remove('hidden');
    setTimeout(() => loadingOverlay.classList.add('active'), 10);
    analyzeBtn.disabled = true;
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pitch_text: pitchText,
                prompt_key: promptType
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            // Store results in sessionStorage
            sessionStorage.setItem('analysisResults', JSON.stringify(data));
            // Redirect to results page
            window.location.href = '/static/results.html';
        } else {
            loadingOverlay.classList.remove('active');
            setTimeout(() => loadingOverlay.classList.add('hidden'), 300);
            alert(`Error: ${data.detail || data.error || 'Analysis failed'}`);
        }
    } catch (error) {
        loadingOverlay.classList.remove('active');
        setTimeout(() => loadingOverlay.classList.add('hidden'), 300);
        alert(`Error: ${error.message}. Make sure the API server is running.`);
    } finally {
        analyzeBtn.disabled = false;
    }
}

function loadExample() {
    const pitchTextarea = document.getElementById('pitch');
    if (pitchTextarea) {
        pitchTextarea.value = `Company: EcoCharge Solutions
Problem: Electric vehicle charging is unreliable, slow, and hard to find in urban areas.
Solution: Smart urban charging pods that integrate with existing parking meters.
Market: $5B addressable market in top 10 US cities.
Traction: 
- 50 pods installed in Boston
- $200K monthly recurring revenue
- 98% uptime rate
- Partnership with 2 major parking operators

Ask: Raising $2M seed round
- 60% for hardware production
- 30% for city expansion
- 10% for team growth

Team:
- CEO: Former Tesla charging infrastructure lead
- CTO: MIT electrical engineering PhD
- COO: Ex-SpotHero operations director`;
    }
}

function clearAll() {
    const pitchTextarea = document.getElementById('pitch');
    if (pitchTextarea) {
        pitchTextarea.value = '';
    }
}

// Make functions globally accessible
window.loadExample = loadExample;
window.clearAll = clearAll;
window.analyzePitch = analyzePitch;
window.previewPrompt = previewPrompt;
window.closePromptPreviewModal = closePromptPreviewModal;

// Close modal on Escape key or clicking outside
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closePromptPreviewModal();
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const promptPreviewModal = document.getElementById('promptPreviewModal');
    if (promptPreviewModal) {
        promptPreviewModal.addEventListener('click', (e) => {
            if (e.target === promptPreviewModal) {
                closePromptPreviewModal();
            }
        });
    }
});
