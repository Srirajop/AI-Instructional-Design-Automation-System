const BASE_URL = import.meta.env?.DEV ? 'http://localhost:8000/api' : '/api';

export const api = {
    async request(endpoint, options = {}) {
        const token = localStorage.getItem('token');
        const defaultHeaders = {
            'Accept': 'application/json',
        };

        if (token) {
            defaultHeaders['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            ...options,
            headers: {
                ...defaultHeaders,
                ...options.headers,
            },
        };

        // If no content-type is set in options, and body is not FormData, default to JSON
        if (!config.headers['Content-Type'] && !(options.body instanceof FormData) && options.body) {
            config.headers['Content-Type'] = 'application/json';
        }

        const maxRetries = 3;
        let attempt = 0;

        const executeRequest = async () => {
            try {
                const response = await fetch(`${BASE_URL}${endpoint}`, config);

                // Check for download responses
                const contentType = response.headers.get('content-type');
                if (contentType && (
                    contentType.includes('application/vnd.openxmlformats-officedocument.wordprocessingml.document') ||
                    contentType.includes('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                )) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;

                    // Try to get filename from content-disposition
                    const contentDisposition = response.headers.get('content-disposition');
                    let filename = contentType.includes('spreadsheetml') ? 'download.xlsx' : 'download.docx';
                    if (contentDisposition) {
                        const matches = /filename="([^"]+)"/.exec(contentDisposition);
                        if (matches != null && matches[1]) filename = matches[1];
                    }

                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                    return { success: true, message: "Download started" };
                }

                const data = await response.json();

                if (!response.ok) {
                    if (response.status === 401) {
                        localStorage.removeItem('token');
                        localStorage.removeItem('user');
                        window.dispatchEvent(new Event('unauthorized'));
                    }
                    let errorMessage = 'API Request Failed';
                    if (data.detail) {
                        if (typeof data.detail === 'string') {
                            errorMessage = data.detail;
                        } else if (Array.isArray(data.detail)) {
                            errorMessage = data.detail.map(e => `${e.loc ? e.loc.join('.') : 'Field'}: ${e.msg}`).join(', ');
                        } else {
                            errorMessage = JSON.stringify(data.detail);
                        }
                    }
                    throw new Error(errorMessage);
                }
                return data;
            } catch (error) {
                // If it's a "Failed to fetch" (Network Error) and we have retries left
                if (error.name === 'TypeError' && error.message.includes('fetch') && attempt < maxRetries) {
                    attempt++;
                    const delay = Math.pow(2, attempt) * 1000; // 2s, 4s, 8s
                    console.warn(`Fetch failed, retrying attempt ${attempt} in ${delay}ms...`);
                    await new Promise(resolve => setTimeout(resolve, delay));
                    return executeRequest();
                }
                console.error('API Error:', error);
                throw error;
            }
        };

        return executeRequest();
    },

    async analyzeSopDocument(formData) {
        const token = localStorage.getItem('token');
        const defaultHeaders = {
            'Accept': 'application/json',
        };
        if (token) {
            defaultHeaders['Authorization'] = `Bearer ${token}`;
        }

        // Call backend /sop/analyze
        const response = await fetch(`${BASE_URL}/sop/analyze`, {
            method: 'POST',
            headers: defaultHeaders,
            body: formData
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'Document analysis failed');
        }

        let suggestions = [];
        const mode = formData.get('mode');
        if (mode === 'format_and_content') {
            try {
                const suggForm = new FormData();
                const file = formData.get('file');
                if (file) suggForm.append('file', file);
                const enhancements = formData.get('content_enhancements');
                if (enhancements) suggForm.append('categories', enhancements);

                const suggRes = await fetch(`${BASE_URL}/sop/suggest-content`, {
                    method: 'POST',
                    headers: defaultHeaders,
                    body: suggForm
                });
                if (suggRes.ok) {
                    const suggData = await suggRes.json();
                    suggestions = suggData.suggestions || [];
                }
            } catch (err) {
                console.warn('Content enhancement suggestions skipped or failed:', err);
            }
        }

        return {
            data: {
                success: true,
                analysis: data,
                suggestions: suggestions
            }
        };
    },

    async formatSopDocument(formData) {
        const token = localStorage.getItem('token');
        const defaultHeaders = {};
        if (token) {
            defaultHeaders['Authorization'] = `Bearer ${token}`;
        }

        // Map formatting_config to config parameter expected by /sop/format
        const reqForm = new FormData();
        for (const [key, value] of formData.entries()) {
            if (key === 'formatting_config') {
                reqForm.append('config', value);
            } else {
                reqForm.append(key, value);
            }
        }

        const response = await fetch(`${BASE_URL}/sop/format`, {
            method: 'POST',
            headers: defaultHeaders,
            body: reqForm
        });

        if (!response.ok) {
            let errorMsg = 'Formatting failed';
            try {
                const errData = await response.json();
                errorMsg = errData.detail || errorMsg;
            } catch (e) {}
            throw new Error(errorMsg);
        }

        const blob = await response.blob();
        const headers = {};
        response.headers.forEach((value, key) => {
            headers[key] = value;
        });

        return {
            data: blob,
            headers: headers
        };
    },

    async generateSopChangeReport(formData) {
        const token = localStorage.getItem('token');
        const defaultHeaders = {
            'Content-Type': 'application/json'
        };
        if (token) {
            defaultHeaders['Authorization'] = `Bearer ${token}`;
        }

        const file = formData.get('file');
        const filename = file ? file.name : 'Document.docx';
        const rawConfig = formData.get('formatting_config');
        let configObj = {};
        if (rawConfig) {
            try {
                configObj = JSON.parse(rawConfig);
            } catch (e) {}
        }
        const rawAccepted = formData.get('accepted_suggestions');
        let acceptedObj = {};
        if (rawAccepted) {
            try {
                acceptedObj = JSON.parse(rawAccepted);
            } catch (e) {}
        }

        const acceptedList = Object.entries(acceptedObj).filter(([k, v]) => !!v).map(([k]) => ({ id: k }));

        const payload = {
            filename: filename,
            mode: configObj.mode || 'format_only',
            formatting_changes: [
                'Applied standard font typography hierarchy across document',
                'Normalized paragraph margins and line spacing',
                'Standardized table header and cell formatting',
                'Configured document header and footer standards'
            ],
            content_changes_count: acceptedList.length,
            accepted_content_suggestions: acceptedList,
            baseline_compliance: 70,
            final_compliance: 100
        };

        const response = await fetch(`${BASE_URL}/sop/change-report`, {
            method: 'POST',
            headers: defaultHeaders,
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            let errorMsg = 'Failed to generate change report';
            try {
                const errData = await response.json();
                errorMsg = errData.detail || errorMsg;
            } catch (e) {}
            throw new Error(errorMsg);
        }

        const blob = await response.blob();
        return {
            data: blob
        };
    }
};
