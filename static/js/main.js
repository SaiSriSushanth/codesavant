// Main JavaScript for CodeSavant Platform

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize CodeMirror editor if we're on the code editor page
    const codeEditorTextarea = document.getElementById('code-editor');
    if (codeEditorTextarea) {
        initializeCodeEditor();
    }

    // Initialize tooltips and popovers if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined') {
        // Initialize tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });

        // Initialize popovers
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }

    // Setup event listeners for the code analysis buttons
    setupAnalysisButtons();
});

/**
 * Initialize the CodeMirror editor with appropriate settings
 */
function initializeCodeEditor() {
    const codeEditorTextarea = document.getElementById('code-editor');
    const languageSelect = document.getElementById('language-select');
    
    // Default language
    let mode = 'python';
    
    // If language select exists, get the selected language
    if (languageSelect) {
        mode = getLanguageMode(languageSelect.value);
        
        // Update mode when language changes
        languageSelect.addEventListener('change', function() {
            editor.setOption('mode', getLanguageMode(this.value));
        });
    }
    
    // Initialize CodeMirror
    const editor = CodeMirror.fromTextArea(codeEditorTextarea, {
        lineNumbers: true,
        mode: mode,
        theme: 'dracula',
        indentUnit: 4,
        smartIndent: true,
        tabSize: 4,
        indentWithTabs: false,
        lineWrapping: false,
        gutters: ["CodeMirror-linenumbers"],
        extraKeys: {
            "Tab": function(cm) {
                cm.replaceSelection(" ".repeat(cm.getOption("indentUnit")));
            }
        }
    });
    
    // Make the editor responsive
    editor.setSize(null, "100%");
    
    // Store the editor instance globally for access from other functions
    window.codeEditor = editor;
    
    // Add event listener for code changes to enable/disable the analyze button
    editor.on('change', function() {
        const analyzeBtn = document.getElementById('analyze-btn');
        if (analyzeBtn) {
            analyzeBtn.disabled = editor.getValue().trim() === '';
        }
    });
    
    return editor;
}

/**
 * Map language selection to CodeMirror mode
 */
function getLanguageMode(language) {
    const modeMap = {
        'python': 'python',
        'javascript': 'javascript',
        'java': 'text/x-java',
        'cpp': 'text/x-c++src',
        'csharp': 'text/x-csharp',
        'php': 'php',
        'ruby': 'ruby',
        'go': 'go',
        'swift': 'text/x-swift',
        'kotlin': 'text/x-kotlin'
    };
    return modeMap[language.toLowerCase()] || 'python';
}

/**
 * Setup event listeners for the code analysis buttons
 */
function setupAnalysisButtons() {
    // Analyze Code button
    const analyzeBtn = document.getElementById('analyze-btn');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', function() {
            analyzeCode('analyze');
        });
    }
    
    // Optimize Code button
    const optimizeBtn = document.getElementById('optimize-btn');
    if (optimizeBtn) {
        optimizeBtn.addEventListener('click', function() {
            analyzeCode('optimize');
        });
    }
    
    // Explain Code button
    const explainBtn = document.getElementById('explain-btn');
    if (explainBtn) {
        explainBtn.addEventListener('click', function() {
            analyzeCode('explain');
        });
    }
    
    // Debug Code button
    const debugBtn = document.getElementById('debug-btn');
    if (debugBtn) {
        debugBtn.addEventListener('click', function() {
            analyzeCode('debug');
        });
    }
    
    // Get Learning Resources button
    const resourcesBtn = document.getElementById('resources-btn');
    if (resourcesBtn) {
        resourcesBtn.addEventListener('click', function() {
            getLearningResources();
        });
    }
    
    // Get Coding Challenge button
    const challengeBtn = document.getElementById('challenge-btn');
    if (challengeBtn) {
        challengeBtn.addEventListener('click', function() {
            getCodingChallenge();
        });
    }
}

/**
 * Send code to the backend for analysis
 */
function analyzeCode(analysisType) {
    // Get the code from CodeMirror
    const code = window.codeEditor.getValue();
    const language = document.getElementById('language-select').value;
    
    // Show loading state
    const aiResponseElement = document.getElementById('ai-response');
    aiResponseElement.innerHTML = '<div class="text-center py-5"><div class="spinner"></div><p class="mt-3">Analyzing your code with GPT-4-Turbo...</p></div>';
    
    // Disable buttons during analysis
    toggleAnalysisButtons(true);
    
    // Prepare the request data
    const requestData = {
        code: code,
        language: language,
        action: analysisType
    };
    
    // Send the request to the backend
    fetch('/api/analyze-code/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Display the AI response
        displayAIResponse(data.feedback);
    })
    .catch(error => {
        console.error('Error:', error);
        aiResponseElement.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
    })
    .finally(() => {
        // Re-enable buttons
        toggleAnalysisButtons(false);
    });
}

/**
 * Get learning resources based on the current code
 */
function getLearningResources() {
    // Get the code from CodeMirror
    const code = window.codeEditor.getValue();
    const language = document.getElementById('language-select').value;
    
    // Show loading state
    const aiResponseElement = document.getElementById('ai-response');
    aiResponseElement.innerHTML = '<div class="text-center py-5"><div class="spinner"></div><p class="mt-3">Finding personalized learning resources...</p></div>';
    
    // Disable buttons during request
    toggleAnalysisButtons(true);
    
    // Prepare the request data
    const requestData = {
        code: code,
        language: language
    };
    
    // Send the request to the backend
    fetch('/api/get-learning-resources/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Display the learning resources
        displayLearningResources(data.resources);
    })
    .catch(error => {
        console.error('Error:', error);
        aiResponseElement.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
    })
    .finally(() => {
        // Re-enable buttons
        toggleAnalysisButtons(false);
    });
}

/**
 * Get a coding challenge based on the current code and skill level
 */
function getCodingChallenge() {
    // Get the code from CodeMirror
    const code = window.codeEditor.getValue();
    const language = document.getElementById('language-select').value;
    
    // Show loading state
    const aiResponseElement = document.getElementById('ai-response');
    aiResponseElement.innerHTML = '<div class="text-center py-5"><div class="spinner"></div><p class="mt-3">Generating a personalized coding challenge...</p></div>';
    
    // Disable buttons during request
    toggleAnalysisButtons(true);
    
    // Prepare the request data
    const requestData = {
        code: code,
        language: language
    };
    
    // Send the request to the backend
    fetch('/api/get-coding-challenge/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Display the coding challenge
        displayCodingChallenge(data.challenge);
    })
    .catch(error => {
        console.error('Error:', error);
        aiResponseElement.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
    })
    .finally(() => {
        // Re-enable buttons
        toggleAnalysisButtons(false);
    });
}

/**
 * Display the AI response with proper formatting
 */
function displayAIResponse(feedback) {
    const aiResponseElement = document.getElementById('ai-response');
    
    // Use a markdown parser to format the response
    if (typeof marked !== 'undefined') {
        aiResponseElement.innerHTML = marked.parse(feedback);
    } else {
        // Fallback if marked.js is not available
        aiResponseElement.innerHTML = `<pre>${feedback}</pre>`;
    }
    
    // Add syntax highlighting to code blocks if Prism is available
    if (typeof Prism !== 'undefined') {
        Prism.highlightAllUnder(aiResponseElement);
    }
    
    // Add a save button if not already present
    if (!document.getElementById('save-snippet-btn')) {
        const saveBtn = document.createElement('button');
        saveBtn.id = 'save-snippet-btn';
        saveBtn.className = 'btn btn-success mt-3';
        saveBtn.innerHTML = '<i class="fas fa-save"></i> Save Snippet';
        saveBtn.addEventListener('click', openSaveSnippetModal);
        
        aiResponseElement.appendChild(document.createElement('hr'));
        aiResponseElement.appendChild(saveBtn);
    }
}

/**
 * Display learning resources in a card format
 */
function displayLearningResources(resources) {
    const aiResponseElement = document.getElementById('ai-response');
    
    let html = '<h4>Personalized Learning Resources</h4>';
    html += '<p>Based on your code, here are some resources that might help you improve:</p>';
    html += '<div class="row">';
    
    resources.forEach(resource => {
        html += `
        <div class="col-md-6 mb-4">
            <div class="card resource-card h-100">
                <div class="card-body">
                    <span class="resource-type ${resource.type.toLowerCase()}">${resource.type}</span>
                    <h5 class="card-title">${resource.title}</h5>
                    <p class="card-text">${resource.description}</p>
                </div>
                <div class="card-footer bg-white">
                    <a href="${resource.url}" target="_blank" class="btn btn-sm btn-primary">View Resource</a>
                </div>
            </div>
        </div>
        `;
    });
    
    html += '</div>';
    aiResponseElement.innerHTML = html;
}

/**
 * Display a coding challenge
 */
function displayCodingChallenge(challenge) {
    const aiResponseElement = document.getElementById('ai-response');
    
    let difficultyClass = '';
    switch (challenge.difficulty.toLowerCase()) {
        case 'easy':
            difficultyClass = 'difficulty-easy';
            break;
        case 'medium':
            difficultyClass = 'difficulty-medium';
            break;
        case 'hard':
            difficultyClass = 'difficulty-hard';
            break;
    }
    
    let html = `
    <div class="card challenge-card mb-4">
        <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Coding Challenge</h5>
            <span class="challenge-difficulty ${difficultyClass}">${challenge.difficulty}</span>
        </div>
        <div class="card-body">
            <h5>${challenge.title}</h5>
            <p>${challenge.description}</p>
            
            <div class="mt-4">
                <h6>Requirements:</h6>
                <ul>
    `;
    
    challenge.requirements.forEach(req => {
        html += `<li>${req}</li>`;
    });
    
    html += `
                </ul>
            </div>
            
            <div class="mt-4">
                <h6>Example:</h6>
                <pre><code class="language-${challenge.language.toLowerCase()}">${challenge.example}</code></pre>
            </div>
            
            <div class="mt-4">
                <button id="start-challenge-btn" class="btn btn-primary">Start Challenge</button>
            </div>
        </div>
    </div>
    `;
    
    aiResponseElement.innerHTML = html;
    
    // Add syntax highlighting to code blocks if Prism is available
    if (typeof Prism !== 'undefined') {
        Prism.highlightAllUnder(aiResponseElement);
    }
    
    // Add event listener to the start challenge button
    const startChallengeBtn = document.getElementById('start-challenge-btn');
    if (startChallengeBtn) {
        startChallengeBtn.addEventListener('click', function() {
            // Clear the editor and insert the challenge template
            window.codeEditor.setValue(`# ${challenge.title}\n# ${challenge.difficulty} Challenge\n\n# TODO: Implement your solution here\n\n`);
            
            // Focus on the editor
            window.codeEditor.focus();
            
            // Set cursor position after the TODO comment
            window.codeEditor.setCursor(window.codeEditor.lineCount(), 0);
        });
    }
}

/**
 * Toggle the disabled state of all analysis buttons
 */
function toggleAnalysisButtons(disabled) {
    const buttons = [
        'analyze-btn',
        'optimize-btn',
        'explain-btn',
        'debug-btn',
        'resources-btn',
        'challenge-btn'
    ];
    
    buttons.forEach(btnId => {
        const btn = document.getElementById(btnId);
        if (btn) {
            btn.disabled = disabled;
        }
    });
}

/**
 * Open the save snippet modal
 */
function openSaveSnippetModal() {
    // Get the code and language
    const code = window.codeEditor.getValue();
    const language = document.getElementById('language-select').value;
    const feedback = document.getElementById('ai-response').innerHTML;
    
    // Create a modal if it doesn't exist
    let modal = document.getElementById('save-snippet-modal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'save-snippet-modal';
        modal.className = 'modal fade';
        modal.setAttribute('tabindex', '-1');
        modal.setAttribute('aria-labelledby', 'saveSnippetModalLabel');
        modal.setAttribute('aria-hidden', 'true');
        
        modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="saveSnippetModalLabel">Save Code Snippet</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="save-snippet-form">
                        <div class="mb-3">
                            <label for="snippet-title" class="form-label">Title</label>
                            <input type="text" class="form-control" id="snippet-title" required>
                        </div>
                        <div class="mb-3">
                            <label for="snippet-description" class="form-label">Description (optional)</label>
                            <textarea class="form-control" id="snippet-description" rows="3"></textarea>
                        </div>
                        <input type="hidden" id="snippet-code">
                        <input type="hidden" id="snippet-language">
                        <input type="hidden" id="snippet-feedback">
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" id="save-snippet-submit">Save</button>
                </div>
            </div>
        </div>
        `;
        
        document.body.appendChild(modal);
    }
    
    // Set the form values
    document.getElementById('snippet-code').value = code;
    document.getElementById('snippet-language').value = language;
    document.getElementById('snippet-feedback').value = feedback;
    
    // Show the modal
    const modalInstance = new bootstrap.Modal(modal);
    modalInstance.show();
    
    // Add event listener to the save button
    const saveBtn = document.getElementById('save-snippet-submit');
    saveBtn.addEventListener('click', saveCodeSnippet);
}

/**
 * Save the code snippet to the database
 */
function saveCodeSnippet() {
    const title = document.getElementById('snippet-title').value;
    const description = document.getElementById('snippet-description').value;
    const code = document.getElementById('snippet-code').value;
    const language = document.getElementById('snippet-language').value;
    const feedback = document.getElementById('snippet-feedback').value;
    
    // Validate the form
    if (!title) {
        alert('Please enter a title for your snippet');
        return;
    }
    
    // Prepare the request data
    const requestData = {
        title: title,
        description: description,
        code: code,
        language: language,
        feedback: feedback
    };
    
    // Send the request to the backend
    fetch('/api/save-snippet/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Close the modal
        const modal = document.getElementById('save-snippet-modal');
        const modalInstance = bootstrap.Modal.getInstance(modal);
        modalInstance.hide();
        
        // Show success message
        const aiResponseElement = document.getElementById('ai-response');
        aiResponseElement.innerHTML += `
        <div class="alert alert-success mt-3">
            <i class="fas fa-check-circle"></i> Snippet saved successfully! 
            <a href="/view-snippet/${data.snippet_id}/" class="alert-link">View it here</a>.
        </div>
        `;
    })
    .catch(error => {
        console.error('Error:', error);
        alert(`Error saving snippet: ${error.message}`);
    });
}

/**
 * Get CSRF token from cookies
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}