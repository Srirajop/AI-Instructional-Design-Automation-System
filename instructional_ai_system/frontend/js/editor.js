const projectId = localStorage.getItem('current_project_id');
if (!projectId) {
    window.location.href = 'dashboard.html';
}

let docContent = "";
let isEditing = false;
let saveTimeout = null;

const previewDiv = document.getElementById('markdown-preview');
const editorTextarea = document.getElementById('markdown-editor');
const generateBtn = document.getElementById('generate-btn');
const actionButtons = document.getElementById('action-buttons');
const studioView = document.getElementById('studio-view');
const loadingOverlay = document.getElementById('loading-overlay');
const saveStatus = document.getElementById('save-status');

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const project = await api.request(`/history/${projectId}`);
        document.getElementById('project-title').innerText = project.title;

        if (project.design_doc) {
            docContent = project.design_doc;
            showStudio();
        } else {
            generateBtn.style.display = 'block';
        }

    } catch (e) {
        alert("Error loading project: " + e.message);
    }
});

function showStudio() {
    generateBtn.style.display = 'none';
    actionButtons.style.display = 'flex';
    studioView.classList.remove('hidden');
    updatePreview(docContent);
    editorTextarea.value = docContent;
}

function updatePreview(text) {
    if (window.marked) {
        // Simple fix for newlines in tables which sometimes get corrupted in marked
        let cleanText = text.replace(/<br>/g, '<br/>');
        previewDiv.innerHTML = marked.parse(cleanText);
    } else {
        previewDiv.innerText = text;
    }
}

generateBtn.addEventListener('click', async () => {
    generateBtn.disabled = true;
    loadingOverlay.classList.remove('hidden');
    try {
        const res = await api.request(`/design/${projectId}/generate`, { method: 'POST' });
        docContent = res.design_doc;
        showStudio();
    } catch (e) {
        alert("Failed to generate: " + e.message);
        generateBtn.disabled = false;
    } finally {
        loadingOverlay.classList.add('hidden');
    }
});

document.getElementById('toggle-edit-btn').addEventListener('click', () => {
    isEditing = !isEditing;
    if (isEditing) {
        previewDiv.style.display = 'none';
        editorTextarea.style.display = 'block';
        document.getElementById('toggle-edit-btn').innerText = 'Save Raw Edit';
    } else {
        docContent = editorTextarea.value;
        previewDiv.style.display = 'block';
        editorTextarea.style.display = 'none';
        document.getElementById('toggle-edit-btn').innerText = 'Toggle Raw Edit';
        updatePreview(docContent);
        autoSaveInline();
    }
});

editorTextarea.addEventListener('input', () => {
    clearTimeout(saveTimeout);
    saveStatus.innerText = 'Unsaved changes...';
});

async function autoSaveInline() {
    saveStatus.innerText = 'Saving...';
    try {
        await api.request(`/edit/save-inline?doc_type=design&project_id=${projectId}`, {
            method: 'POST',
            body: JSON.stringify({ content: docContent })
        });
        saveStatus.innerText = 'Saved automatically';
        setTimeout(() => saveStatus.innerText = '', 2000);
    } catch (e) {
        saveStatus.innerText = 'Save failed';
        saveStatus.style.color = 'var(--danger)';
    }
}

document.getElementById('download-btn').addEventListener('click', async () => {
    await api.request(`/export/${projectId}/design-doc`, { method: 'GET' });
});

// Chat Logic
const chatSendBtn = document.getElementById('chat-send-btn');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');

function appendMessage(role, text) {
    const div = document.createElement('div');
    div.className = `msg ${role}`;
    // Simple basic text rendering for chat
    div.innerHTML = text.replace(/\n/g, '<br>');
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatSendBtn.addEventListener('click', async () => {
    const text = chatInput.value.trim();
    if (!text) return;

    appendMessage('user', text);
    chatInput.value = '';
    chatSendBtn.disabled = true;
    const loadingId = 'loading-' + Date.now();

    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'msg ai text-muted';
    loadingDiv.id = loadingId;
    loadingDiv.innerText = 'Thinking and editing...';
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const payload = {
            doc_type: "design",
            user_prompt: text,
            current_content: docContent
        };

        const res = await api.request(`/edit/chat?project_id=${projectId}`, {
            method: 'POST',
            body: JSON.stringify(payload)
        });

        document.getElementById(loadingId).remove();
        appendMessage('ai', res.assistant_reply);

        if (res.updated_document !== docContent) {
            docContent = res.updated_document;
            editorTextarea.value = docContent;
            updatePreview(docContent);
            saveStatus.innerText = 'Document automatically updated by AI';
            setTimeout(() => saveStatus.innerText = '', 3000);
        }

    } catch (e) {
        document.getElementById(loadingId).remove();
        appendMessage('ai', "Error connecting to AI: " + e.message);
    } finally {
        chatSendBtn.disabled = false;
    }
});
