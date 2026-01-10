const API_URL = ""; // Relative path for same-origin serving

const chatHistory = document.getElementById('chat-history');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const pdfUpload = document.getElementById('pdf-upload');
const uploadStatus = document.getElementById('upload-status');

// Handle File Upload
pdfUpload.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.type !== 'application/pdf') {
        uploadStatus.textContent = "Error: Only PDFs allowed.";
        uploadStatus.style.color = "red";
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    uploadStatus.textContent = "Uploading & Processing...";
    uploadStatus.style.color = "#9ca3af";

    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            uploadStatus.textContent = `✓ Ready! (${data.chunks} chunks)`;
            uploadStatus.style.color = "#166534";
        } else {
            uploadStatus.textContent = `Error: ${data.detail || "Upload failed."}`;
            uploadStatus.style.color = "red";
            console.error("Server Error:", data);
        }
    } catch (error) {
        console.error("Network Error:", error);
        uploadStatus.textContent = "Error: Could not connect to server.";
        uploadStatus.style.color = "red";
    }
});

// Handle Chat Logic
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    // Add User Message
    addMessage(message, 'user');
    userInput.value = '';
    sendBtn.disabled = true;

    // Add Loading Indicator
    const loadingId = addLoadingIndicator();

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) throw new Error("Network response was not ok");

        const data = await response.json();

        // Remove Loading Indicator
        removeMessage(loadingId);

        // Add Bot Message
        addMessage(data.answer, 'bot', data.sources);
    } catch (error) {
        console.error(error);
        removeMessage(loadingId);
        addMessage("Sorry, I encountered an error connecting to the server.", 'bot');
    } finally {
        sendBtn.disabled = false;
        userInput.focus();
    }
});

function addMessage(text, sender, sources = []) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;

    let content = `<div class="bubble">${marked.parse(text)}</div>`; // Using marked.js for markdown rendering if available, else plain text
    // For this vanilla version, we'll try a simple text replace for newlines or just textContent if marked isn't loaded
    // We will load marked.js via CDN in index.html for better formatting

    if (sources && sources.length > 0) {
        const uniqueSources = [...new Set(sources)];
        content += `<div class="sources">Sources: ${uniqueSources.join(', ')}</div>`;
    }

    msgDiv.innerHTML = content;
    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function addLoadingIndicator() {
    const id = 'loading-' + Date.now();
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message bot';
    msgDiv.id = id;
    msgDiv.innerHTML = `
        <div class="bubble">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return id;
}

function removeMessage(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}
