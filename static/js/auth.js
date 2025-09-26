// Authentication JavaScript for MARS
class AuthManager {
    constructor() {
        this.currentUser = null;
        this.init();
    }

    init() {
        // Check if user is already logged in
        this.checkAuthState();
        this.setupEventListeners();
    }

    checkAuthState() {
        // Simulate Firebase auth state check
        const savedUser = localStorage.getItem('mars_user');
        if (savedUser) {
            this.currentUser = JSON.parse(savedUser);
            this.redirectToMain();
        }
    }

    setupEventListeners() {
        // Login form
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }

        // Signup form
        const signupForm = document.getElementById('signup-form');
        if (signupForm) {
            signupForm.addEventListener('submit', (e) => this.handleSignup(e));
        }

        // Google signin buttons
        const googleButtons = document.querySelectorAll('.google-signin');
        googleButtons.forEach(button => {
            button.addEventListener('click', () => this.handleGoogleSignin());
        });

        // Form toggle buttons
        const toggleButtons = document.querySelectorAll('.toggle-button');
        toggleButtons.forEach(button => {
            button.addEventListener('click', (e) => this.toggleForms(e));
        });
    }

    async handleLogin(e) {
        e.preventDefault();
        
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        
        if (!email || !password) {
            this.showError('Please fill in all fields');
            return;
        }

        this.showLoading('login-btn', 'Signing in...');

        try {
            // Simulate Firebase authentication
            await this.simulateAuth(email, password);
            
            const user = {
                email: email,
                displayName: email.split('@')[0],
                uid: 'user_' + Date.now(),
                authMethod: 'email'
            };

            this.setCurrentUser(user);
            this.showSuccess('Login successful! Redirecting...');
            
            setTimeout(() => {
                this.redirectToMain();
            }, 1500);

        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading('login-btn', 'Sign In');
        }
    }

    async handleSignup(e) {
        e.preventDefault();
        
        const email = document.getElementById('signup-email').value;
        const password = document.getElementById('signup-password').value;
        const confirmPassword = document.getElementById('signup-confirm-password').value;
        
        if (!email || !password || !confirmPassword) {
            this.showError('Please fill in all fields');
            return;
        }

        if (password !== confirmPassword) {
            this.showError('Passwords do not match');
            return;
        }

        if (password.length < 6) {
            this.showError('Password must be at least 6 characters');
            return;
        }

        this.showLoading('signup-btn', 'Creating account...');

        try {
            // Simulate Firebase authentication
            await this.simulateAuth(email, password, true);
            
            const user = {
                email: email,
                displayName: email.split('@')[0],
                uid: 'user_' + Date.now(),
                authMethod: 'email'
            };

            this.setCurrentUser(user);
            this.showSuccess('Account created successfully! Redirecting...');
            
            setTimeout(() => {
                this.redirectToMain();
            }, 1500);

        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading('signup-btn', 'Create Account');
        }
    }

    async handleGoogleSignin() {
        const button = document.querySelector('.google-signin');
        this.showLoading(button, 'Connecting to Google...');

        try {
            // Simulate Google authentication
            await this.simulateAuth('google');
            
            const user = {
                email: 'user@gmail.com',
                displayName: 'Google User',
                uid: 'google_user_' + Date.now(),
                authMethod: 'google',
                photoURL: 'https://via.placeholder.com/40'
            };

            this.setCurrentUser(user);
            this.showSuccess('Google sign-in successful! Redirecting...');
            
            setTimeout(() => {
                this.redirectToMain();
            }, 1500);

        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading(button, 'Continue with Google');
        }
    }

    async simulateAuth(email, password, isSignup = false) {
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Simulate potential errors
        if (email === 'error@test.com') {
            throw new Error('Invalid credentials');
        }
        
        if (isSignup && email === 'existing@test.com') {
            throw new Error('Email already exists');
        }
        
        return true;
    }

    setCurrentUser(user) {
        this.currentUser = user;
        localStorage.setItem('mars_user', JSON.stringify(user));
    }

    redirectToMain() {
        window.location.href = '/';
    }

    toggleForms(e) {
        e.preventDefault();
        
        const loginContainer = document.getElementById('login-container');
        const signupContainer = document.getElementById('signup-container');
        
        if (loginContainer && signupContainer) {
            if (loginContainer.style.display === 'none') {
                loginContainer.style.display = 'block';
                signupContainer.style.display = 'none';
            } else {
                loginContainer.style.display = 'none';
                signupContainer.style.display = 'block';
            }
        }
    }

    showError(message) {
        this.hideMessages();
        const errorDiv = document.querySelector('.error-message');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                errorDiv.style.display = 'none';
            }, 5000);
        }
    }

    showSuccess(message) {
        this.hideMessages();
        const successDiv = document.querySelector('.success-message');
        if (successDiv) {
            successDiv.textContent = message;
            successDiv.style.display = 'block';
        }
    }

    hideMessages() {
        const errorDiv = document.querySelector('.error-message');
        const successDiv = document.querySelector('.success-message');
        
        if (errorDiv) errorDiv.style.display = 'none';
        if (successDiv) successDiv.style.display = 'none';
    }

    showLoading(buttonElement, text) {
        const button = typeof buttonElement === 'string' 
            ? document.getElementById(buttonElement) 
            : buttonElement;
            
        if (button) {
            button.disabled = true;
            button.innerHTML = `<span class="loading"></span>${text}`;
        }
    }

    hideLoading(buttonElement, originalText) {
        const button = typeof buttonElement === 'string' 
            ? document.getElementById(buttonElement) 
            : buttonElement;
            
        if (button) {
            button.disabled = false;
            button.innerHTML = originalText;
        }
    }

    logout() {
        this.currentUser = null;
        localStorage.removeItem('mars_user');
        window.location.href = '/auth';
    }
}

// Initialize authentication manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.authManager = new AuthManager();
});
