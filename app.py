from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import threading
import os
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from multi_agent_research_system_mars.crew import MultiAgentResearchSystemMarsCrew

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
    
    # Start research in background thread
    def run_research():
        global is_running, current_status
        try:
            is_running = True
            current_status = "Running research..."
            
            inputs = {
                'topic': topic,
                'recipient_email': recipient_email
            }
            
            # Run the crew
            MultiAgentResearchSystemMarsCrew().crew().kickoff(inputs=inputs)
            
            current_status = "Research completed successfully!"
        except Exception as e:
            current_status = f"Error: {str(e)}"
        finally:
            is_running = False
    
    # Start the research thread
    research_thread = threading.Thread(target=run_research)
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
    app.run(debug=True, host='0.0.0.0', port=5000)
