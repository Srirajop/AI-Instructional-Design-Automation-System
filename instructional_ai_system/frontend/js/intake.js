let currentProjectId = null;

document.addEventListener('DOMContentLoaded', () => {
    // Clear project ID when starting new
    localStorage.removeItem('current_project_id');
});

document.getElementById('intake-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('save-intake-btn');
    const status = document.getElementById('intake-status');
    btn.disabled = true;
    btn.innerText = 'Saving...';

    const intakeData = {
        course_title: document.getElementById('course_title').value,
        business_unit: document.getElementById('business_unit').value,
        course_type: document.getElementById('course_type').value,
        target_audience: document.getElementById('target_audience').value,
        objective_1: document.getElementById('objective_1').value,
        objective_2: document.getElementById('objective_2').value,
        objective_3: document.getElementById('objective_3').value,
        interactivity_level: document.getElementById('interactivity_level').value,
        num_modules: parseInt(document.getElementById('num_modules').value)
    };

    try {
        const result = await api.request('/intake/', {
            method: 'POST',
            body: JSON.stringify(intakeData)
        });

        currentProjectId = result.id;
        localStorage.setItem('current_project_id', currentProjectId);

        status.innerText = 'Project details saved! Proceed to Step 2.';
        document.getElementById('step-2').classList.remove('hidden');

        // Disable form
        const inputs = document.querySelectorAll('#intake-form input, #intake-form select');
        inputs.forEach(i => i.disabled = true);
        btn.classList.add('hidden');

    } catch (err) {
        status.style.color = 'var(--danger)';
        status.innerText = 'Error saving project: ' + err.message;
        btn.disabled = false;
        btn.innerText = 'Save Project Details →';
    }
});

document.getElementById('upload-file-btn').addEventListener('click', async () => {
    if (!currentProjectId) return alert("Please save project details first.");
    const fileInput = document.getElementById('file-upload');
    const status = document.getElementById('extraction-status');

    if (!fileInput.files.length) return alert("Please select a file.");

    const btn = document.getElementById('upload-file-btn');
    btn.disabled = true;
    btn.innerText = 'Extracting...';
    status.style.color = 'var(--text-main)';
    status.innerText = 'Parsing file content...';

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const res = await api.request(`/extraction/${currentProjectId}/upload`, {
            method: 'POST',
            body: formData
        });
        status.style.color = 'var(--success)';
        status.innerText = `Content extracted successfully (${res.extracted_length} chars). You can upload more.`;
        fileInput.value = "";
    } catch (err) {
        status.style.color = 'var(--danger)';
        status.innerText = 'Error: ' + err.message;
    } finally {
        btn.disabled = false;
        btn.innerText = 'Upload & Extract';
    }
});

document.getElementById('upload-url-btn').addEventListener('click', async () => {
    if (!currentProjectId) return alert("Please save project details first.");
    const urlInput = document.getElementById('url-upload');
    const status = document.getElementById('extraction-status');
    const url = urlInput.value.trim();

    if (!url) return alert("Please enter a valid URL.");

    const btn = document.getElementById('upload-url-btn');
    btn.disabled = true;
    btn.innerText = 'Extracting...';
    status.style.color = 'var(--text-main)';
    status.innerText = 'Scraping URL/YouTube...';

    const formData = new FormData();
    formData.append("url", url);

    try {
        const res = await api.request(`/extraction/${currentProjectId}/url`, {
            method: 'POST',
            body: formData
        });
        status.style.color = 'var(--success)';
        status.innerText = `Content extracted successfully (${res.extracted_length} chars). You can add more.`;
        urlInput.value = "";
    } catch (err) {
        status.style.color = 'var(--danger)';
        status.innerText = 'Error: ' + err.message;
    } finally {
        btn.disabled = false;
        btn.innerText = 'Extract URL';
    }
});

document.getElementById('continue-btn').addEventListener('click', () => {
    if (!currentProjectId) return alert("Please initialize the project first.");
    window.location.href = 'editor.html';
});
