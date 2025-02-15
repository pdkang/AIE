let sessionId = null;

function setLoading(isLoading, action) {
    const button = document.getElementById(action === 'upload' ? 'uploadButton' : 'queryButton');
    const spinner = document.getElementById(action === 'upload' ? 'uploadSpinner' : 'querySpinner');
    
    if (isLoading) {
        button.classList.add('loading');
        spinner.style.display = 'inline';
        button.disabled = true;
    } else {
        button.classList.remove('loading');
        spinner.style.display = 'none';
        button.disabled = false;
    }
}

async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    
    if (!fileInput.files.length) {
        alert('Please select a file first');
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    setLoading(true, 'upload');
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        sessionId = data.session_id;
        
    } catch (error) {
        alert('Error uploading file: ' + error);
    } finally {
        setLoading(false, 'upload');
    }
}

async function submitQuery() {
    const queryInput = document.getElementById('queryInput');
    
    if (!queryInput.value.trim()) {
        alert('Please enter a question');
        return;
    }

    setLoading(true, 'query');
    
    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                query: queryInput.value
            })
        });
        
        const data = await response.json();
        
        // Show response section and its components
        const responseSection = document.querySelector('.response-section');
        responseSection.style.display = 'block';
        
        // Update and show answer
        const answerElement = document.getElementById('answer');
        answerElement.textContent = data.answer;
        answerElement.style.display = 'block';
        
        // Show switch container
        document.querySelector('.switch-container').style.display = 'block';
        
        // Update context
        document.getElementById('context').innerHTML = data.context.join('<br><br>');
        
        // Show context section if toggle is checked
        if (document.getElementById('contextToggle').checked) {
            document.getElementById('contextSection').style.display = 'block';
        }
        
    } catch (error) {
        alert('Error submitting query: ' + error);
    } finally {
        setLoading(false, 'query');
    }
}

function toggleContext() {
    const contextSection = document.getElementById('contextSection');
    contextSection.style.display = document.getElementById('contextToggle').checked ? 'block' : 'none';
}

// Initialize UI state
document.addEventListener('DOMContentLoaded', function() {
    // Hide all spinners by default
    const spinners = document.querySelectorAll('.spinner');
    spinners.forEach(spinner => {
        spinner.style.display = 'none';
    });
    
    // Show response section but hide context section
    document.querySelector('.response-section').style.display = 'block';
    document.getElementById('contextSection').style.display = 'none';
    
    // Show switch container
    document.querySelector('.switch-container').style.display = 'block';
}); 