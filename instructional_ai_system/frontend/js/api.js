const API_BASE = "http://localhost:8000/api";

const api = {
    getToken() {
        return localStorage.getItem("access_token");
    },

    setToken(token) {
        localStorage.setItem("access_token", token);
    },

    logout() {
        localStorage.removeItem("access_token");
        window.location.href = "index.html";
    },

    async request(endpoint, options = {}) {
        const url = `${API_BASE}${endpoint}`;
        const headers = {
            "Content-Type": "application/json",
            ...options.headers,
        };

        const token = this.getToken();
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        // Remove Content-Type if FormData was passed (browser boundary handling)
        if (options.body instanceof FormData) {
            delete headers["Content-Type"];
        }

        try {
            const response = await fetch(url, { ...options, headers });

            if (response.status === 401 && !endpoint.includes("/login")) {
                this.logout();
                throw new Error("Unauthorized");
            }

            // Check for file download
            if (response.headers.get("Content-Disposition")?.includes("attachment")) {
                const blob = await response.blob();
                const disposition = response.headers.get("Content-Disposition");
                const filenameMatch = disposition.match(/filename=(.+)/);
                const filename = filenameMatch ? filenameMatch[1] : "download.file";

                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(downloadUrl);
                return { success: true };
            }

            const data = await response.json().catch(() => ({}));

            if (!response.ok) {
                throw new Error(data.detail || "API Request Failed");
            }
            return data;
        } catch (error) {
            console.error("API Error:", error);
            throw error;
        }
    }
};

// Protect routes
if (!window.location.pathname.endsWith('index.html') && !window.location.pathname.endsWith('/') && !api.getToken()) {
    api.logout();
}
