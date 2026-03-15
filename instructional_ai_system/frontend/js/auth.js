document.addEventListener('DOMContentLoaded', () => {
    // Redirect to dashboard if already logged in
    if (api.getToken()) {
        window.location.href = 'dashboard.html';
    }
});

function toggleAuth(type) {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const tabLogin = document.getElementById('tab-login');
    const tabRegister = document.getElementById('tab-register');
    const errorMsg = document.getElementById('error-msg');

    errorMsg.classList.add('hidden');

    if (type === 'login') {
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
        tabLogin.classList.add('btn-primary');
        tabLogin.classList.remove('btn-outline');
        tabRegister.classList.add('btn-outline');
        tabRegister.classList.remove('btn-primary');
    } else {
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
        tabRegister.classList.add('btn-primary');
        tabRegister.classList.remove('btn-outline');
        tabLogin.classList.add('btn-outline');
        tabLogin.classList.remove('btn-primary');
    }
}

document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('login-btn');
    btn.disabled = true;
    btn.innerText = 'Logging in...';

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const errorMsg = document.getElementById('error-msg');
    errorMsg.classList.add('hidden');

    try {
        const formData = new URLSearchParams();
        formData.append('username', email); // OAuth2 expects 'username' field
        formData.append('password', password);

        // Not using api.request here because fetch needs application/x-www-form-urlencoded
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData.toString()
        });

        const data = await response.json();

        if (response.ok) {
            api.setToken(data.access_token);
            window.location.href = 'dashboard.html';
        } else {
            errorMsg.innerText = data.detail || 'Login failed';
            errorMsg.classList.remove('hidden');
        }
    } catch (err) {
        errorMsg.innerText = 'Network error. Backend might be down.';
        errorMsg.classList.remove('hidden');
    } finally {
        btn.disabled = false;
        btn.innerText = 'Login';
    }
});

document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('reg-btn');
    btn.disabled = true;
    btn.innerText = 'Registering...';

    const name = document.getElementById('reg-name').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    const errorMsg = document.getElementById('error-msg');
    errorMsg.classList.add('hidden');

    try {
        await api.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ name, email, password })
        });

        alert("Registration successful! Please login.");
        toggleAuth('login');
        document.getElementById('login-email').value = email;
    } catch (err) {
        errorMsg.innerText = err.message || 'Registration failed';
        errorMsg.classList.remove('hidden');
    } finally {
        btn.disabled = false;
        btn.innerText = 'Register';
    }
});
