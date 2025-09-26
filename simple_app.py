from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import threading
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

app = Flask(__name__)
app.secret_key = 'mars-multi-agent-research-system-secret-key-2024'

# Global variable to track running status
is_running = False
current_status = "Ready"

def check_auth():
    """Check if user is authenticated"""
    return 'user' in session or request.headers.get('Authorization')

@app.route('/')
def index():
    # Check authentication
    if not check_auth():
        return redirect(url_for('auth'))
    return render_template('index.html')

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """API endpoint for login (for non-Firebase fallback)"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Simple validation (in production, use proper authentication)
    if email and password:
        session['user'] = {
            'email': email,
            'uid': f"user_{hash(email)}",
            'displayName': email.split('@')[0]
        }
        return jsonify({'success': True, 'message': 'Login successful'})
    
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    """API endpoint for logout"""
    session.pop('user', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/start-research', methods=['POST'])
def start_research():
    global is_running, current_status
    
    # Check authentication
    if not check_auth():
        return jsonify({'error': 'Authentication required'}), 401
    
    if is_running:
        return jsonify({'error': 'Research is already running'}), 400
    
    data = request.get_json()
    topic = data.get('topic')
    recipient_email = data.get('recipient_email')
    
    if not topic or not recipient_email:
        return jsonify({'error': 'Topic and recipient email are required'}), 400
    
    # Simulate research process
    def simulate_research():
        global is_running, current_status
        import time
        try:
            is_running = True
            current_status = "Initializing research agents..."
            time.sleep(2)
            
            current_status = "Technology research in progress..."
            time.sleep(3)
            
            current_status = "Market analysis running..."
            time.sleep(3)
            
            current_status = "Financial analysis in progress..."
            time.sleep(2)
            
            current_status = "Generating comprehensive reports..."
            time.sleep(3)
            
            current_status = "Creating PDF documents..."
            time.sleep(2)
            
            current_status = f"Research completed! Results would be sent to {recipient_email}"
            
        except Exception as e:
            current_status = f"Error: {str(e)}"
        finally:
            is_running = False
    
    # Start the simulation thread
    research_thread = threading.Thread(target=simulate_research)
    research_thread.daemon = True
    research_thread.start()
    
    return jsonify({'message': 'Research started successfully'})

@app.route('/status')
def get_status():
    # Check authentication
    if not check_auth():
        return jsonify({'error': 'Authentication required'}), 401
        
    return jsonify({
        'is_running': is_running,
        'status': current_status
    })

if __name__ == '__main__':
    print("🚀 Starting MARS Web Interface (Demo Mode)...")
    print("=" * 50)
    print("📱 The web interface will be available at: http://localhost:5000")
    print("🔄 Starting Flask server...")
    print()
    app.run(debug=True, host='0.0.0.0', port=5000)
