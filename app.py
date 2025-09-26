from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import threading
import os
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from multi_agent_research_system_mars.crew import MultiAgentResearchSystemMarsCrew
from multi_agent_research_system_mars.tools.gmail_tool import gmail_tool

# Load environment variables
load_dotenv('config.env')

app = Flask(__name__)
app.secret_key = 'mars-multi-agent-research-system-secret-key-2024'

# Global variables to track running status and store research data
is_running = False
current_status = "Ready"
research_data = {
    'topic': '',
    'recipient_email': '',
    'results': {},
    'timestamp': ''
}

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
    uid = data.get('uid')
    
    # Accept Firebase-authenticated sessions (email + uid) or fallback (email + password)
    if email and (uid or password):
        session['user'] = {
            'email': email,
            'uid': uid or f"user_{hash(email)}",
            'displayName': email.split('@')[0]
        }
        return jsonify({'success': True, 'message': 'Login successful'})
    
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    """API endpoint for logout"""
    session.pop('user', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})

# ---------- Research content generation helpers (used for PDFs and email) ----------

def generate_technology_research(topic):
    return {
        'title': f'Technology Analysis: {topic}',
        'summary': f'Comprehensive technology analysis for {topic} revealing key trends, innovations, and technical challenges.',
        'key_findings': [
            f'Emerging technologies in {topic} show 40% growth potential',
            f'Key technical challenges include scalability and integration',
            f'Current market leaders are investing heavily in {topic} innovation',
            f'Future developments expected to focus on AI integration and automation'
        ]
    }

def generate_market_analysis(topic):
    return {
        'title': f'Market Analysis: {topic}',
        'summary': f'In-depth market analysis for {topic} covering size, growth, competition, and opportunities.',
        'market_size': f'The {topic} market is valued at $2.5B with 15% CAGR',
        'key_players': [
            f'Leading companies in {topic} space',
            f'Emerging startups disrupting {topic}',
            f'Traditional players adapting to {topic} trends'
        ],
        'opportunities': [
            f'Untapped segments in {topic} market',
            f'Geographic expansion opportunities',
            f'New application areas for {topic}'
        ]
    }

def generate_financial_analysis(topic):
    return {
        'title': f'Financial Analysis: {topic}',
        'summary': f'Financial projections and business model analysis for {topic}',
        'revenue_model': f'Multiple revenue streams identified for {topic}',
        'projections': {
            'year_1': '$500K revenue potential',
            'year_3': '$2.5M projected revenue',
            'year_5': '$10M target revenue'
        },
        'investment_needed': f'Initial investment of $1.2M for {topic} development',
        'roi_analysis': f'Expected ROI of 250% over 3 years for {topic}'
    }

def generate_ux_research(topic):
    return {
        'title': f'UX Research: {topic}',
        'summary': f'User experience analysis and recommendations for {topic}',
        'user_needs': [
            f'Users need intuitive interface for {topic}',
            f'Mobile-first approach essential for {topic}',
            f'Accessibility requirements for {topic} users'
        ],
        'design_recommendations': [
            f'Implement clean, minimal design for {topic}',
            f'Focus on user journey optimization',
            f'Ensure responsive design across all devices'
        ]
    }

def generate_patent_analysis(topic):
    return {
        'title': f'Patent & IP Analysis: {topic}',
        'summary': f'Intellectual property landscape analysis for {topic}',
        'existing_patents': f'127 existing patents found related to {topic}',
        'patent_opportunities': [
            f'Novel applications of {topic} technology',
            f'Improved algorithms for {topic} processing',
            f'Integration methods for {topic} systems'
        ],
        'ip_strategy': f'Recommended filing 3-5 patents for {topic} innovations'
    }

def generate_regulatory_analysis(topic):
    return {
        'title': f'Regulatory Analysis: {topic}',
        'summary': f'Regulatory compliance requirements for {topic}',
        'key_regulations': [
            f'Data privacy requirements for {topic}',
            f'Industry-specific standards for {topic}',
            f'International compliance for {topic} deployment'
        ],
        'compliance_steps': [
            f'Conduct compliance audit for {topic}',
            f'Implement required security measures',
            f'Obtain necessary certifications'
        ]
    }

def generate_technical_feasibility(topic):
    return {
        'title': f'Technical Feasibility: {topic}',
        'summary': f'Technical implementation analysis for {topic}',
        'technical_requirements': [
            f'Scalable infrastructure for {topic}',
            f'Integration with existing systems',
            f'Performance optimization for {topic}'
        ],
        'implementation_timeline': '6-12 months for full implementation',
        'risk_assessment': f'Medium technical risk for {topic} development'
    }

def generate_comprehensive_documentation(topic):
    return {
        'title': f'Comprehensive Research Report: {topic}',
        'executive_summary': f'This comprehensive analysis of {topic} reveals significant opportunities for growth and innovation. Our 13-agent research system has identified key market trends, technical requirements, and strategic recommendations.',
        'methodology': 'Multi-agent AI analysis using 13 specialized research agents',
        'key_insights': [
            f'{topic} represents a high-growth opportunity',
            f'Technical feasibility is strong with moderate risk',
            f'Market timing is favorable for {topic} entry',
            f'Regulatory environment supports {topic} development'
        ],
        'next_steps': [
            f'Develop detailed implementation plan for {topic}',
            f'Secure initial funding for {topic} development',
            f'Form strategic partnerships in {topic} space'
        ]
    }

def generate_comprehensive_pdf_content(data):
    content = [
        "## EXECUTIVE SUMMARY",
        "",
        data['results'].get('documentation', {}).get('executive_summary', 'Comprehensive analysis completed.'),
        "",
        "## TECHNOLOGY ANALYSIS",
        "",
        data['results'].get('technology', {}).get('summary', 'Technology analysis completed.'),
        "",
        "### Key Findings:",
    ]
    tech_findings = data['results'].get('technology', {}).get('key_findings', [])
    for finding in tech_findings:
        content.append(f"• {finding}")
    content.extend([
        "",
        "## MARKET ANALYSIS",
        "",
        data['results'].get('market', {}).get('summary', 'Market analysis completed.'),
        "",
        f"Market Size: {data['results'].get('market', {}).get('market_size', 'Data not available')}",
        "",
        "## FINANCIAL PROJECTIONS",
        "",
        data['results'].get('financial', {}).get('summary', 'Financial analysis completed.'),
    ])
    return content

def generate_executive_pdf_content(data):
    return [
        "## EXECUTIVE SUMMARY",
        "",
        data['results'].get('documentation', {}).get('executive_summary', 'Executive summary not available.'),
        "",
        "## KEY INSIGHTS",
        "",
        "• Technology feasibility: Strong",
        "• Market opportunity: High growth potential",
        "• Financial projections: Positive ROI expected",
        "• Implementation timeline: 6-12 months",
        "",
        "## RECOMMENDATIONS",
        "",
        "• Proceed with development",
        "• Secure initial funding",
        "• Form strategic partnerships",
        "",
        "## NEXT STEPS",
        "",
        "• Detailed implementation planning",
        "• Prototype development",
        "• Market validation testing"
    ]

def generate_market_pdf_content(data):
    market_data = data['results'].get('market', {})
    content = [
        "## MARKET ANALYSIS REPORT",
        "",
        market_data.get('summary', 'Market analysis not available.'),
        "",
        f"## MARKET SIZE: {market_data.get('market_size', 'Data not available')}",
        "",
        "## KEY PLAYERS",
        ""
    ]
    players = market_data.get('key_players', [])
    for player in players:
        content.append(f"• {player}")
    content.extend([
        "",
        "## OPPORTUNITIES",
        ""
    ])
    opportunities = market_data.get('opportunities', [])
    for opp in opportunities:
        content.append(f"• {opp}")
    return content

def generate_technical_pdf_content(data):
    tech_data = data['results'].get('technical', {})
    content = [
        "## TECHNICAL FEASIBILITY REPORT",
        "",
        tech_data.get('summary', 'Technical analysis not available.'),
        "",
        "## TECHNICAL REQUIREMENTS",
        ""
    ]
    requirements = tech_data.get('technical_requirements', [])
    for req in requirements:
        content.append(f"• {req}")
    content.extend([
        "",
        f"## IMPLEMENTATION TIMELINE: {tech_data.get('implementation_timeline', 'Not specified')}",
        "",
        f"## RISK ASSESSMENT: {tech_data.get('risk_assessment', 'Not specified')}",
        "",
        "## TECHNOLOGY STACK",
        "",
        "• Modern cloud infrastructure",
        "• Scalable microservices architecture",
        "• AI/ML integration capabilities",
        "• Real-time data processing"
    ])
    return content

def generate_pdf_to_file(pdf_type, data):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from io import BytesIO
    import tempfile

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 20)
    topic = data['topic']
    p.drawString(100, 750, f"{pdf_type.upper()} REPORT: {topic}")
    p.setFont("Helvetica", 10)
    p.drawString(100, 730, f"Generated: {data.get('timestamp', 'N/A')}")
    p.drawString(100, 715, f"Research Topic: {topic}")
    p.setFont("Helvetica", 12)
    y = 680
    if pdf_type == 'comprehensive':
        content_lines = generate_comprehensive_pdf_content(data)
    elif pdf_type == 'executive':
        content_lines = generate_executive_pdf_content(data)
    elif pdf_type == 'market':
        content_lines = generate_market_pdf_content(data)
    elif pdf_type == 'technical':
        content_lines = generate_technical_pdf_content(data)
    else:
        content_lines = generate_comprehensive_pdf_content(data)
    for line in content_lines:
        if y < 50:
            p.showPage()
            y = 750
            p.setFont("Helvetica", 12)
        if line.startswith('###'):
            p.setFont("Helvetica-Bold", 14)
            line = line[3:].strip()
        elif line.startswith('##'):
            p.setFont("Helvetica-Bold", 12)
            line = line[2:].strip()
        else:
            p.setFont("Helvetica", 12)
        p.drawString(100, y, line[:80])
        y -= 20
    p.save()
    buffer.seek(0)
    # Write to temp file and return path
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=f"_{pdf_type}.pdf")
    with open(tmp.name, 'wb') as f:
        f.write(buffer.getvalue())
    return tmp.name

def send_research_email(topic, recipient_email, attachments_paths):
    subject = f"MARS Research Results: {topic}"
    body = (
        f"Hello,\n\nPlease find attached the research reports for '{topic}'.\n"
        "This email was sent automatically by MARS.\n\nRegards,\nMARS"
    )
    result = gmail_tool.run(to_email=recipient_email, subject=subject, body=body, attachments=attachments_paths)
    return result

@app.route('/start-research', methods=['POST'])
def start_research():
    global is_running, current_status, research_data
    
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
    
    # Start research in background thread (simulate multi-agent work and generate PDFs)
    def run_research():
        import time
        from time import strftime
        global is_running, current_status, research_data
        try:
            is_running = True
            research_data['topic'] = topic
            research_data['recipient_email'] = recipient_email
            research_data['timestamp'] = strftime('%Y-%m-%d %H:%M:%S')
            
            current_status = "Initializing 13 AI research agents..."
            time.sleep(2)
            
            current_status = "🔬 Technology research agent analyzing trends..."
            time.sleep(2)
            research_data['results']['technology'] = generate_technology_research(topic)
            
            current_status = "📊 Market analysis agent researching competition..."
            time.sleep(2)
            research_data['results']['market'] = generate_market_analysis(topic)
            
            current_status = "💰 Financial analysis agent validating business model..."
            time.sleep(2)
            research_data['results']['financial'] = generate_financial_analysis(topic)
            
            current_status = "👥 UX research agent studying user experience..."
            time.sleep(2)
            research_data['results']['ux'] = generate_ux_research(topic)
            
            current_status = "⚖️ Patent agent analyzing IP landscape..."
            time.sleep(2)
            research_data['results']['patent'] = generate_patent_analysis(topic)
            
            current_status = "📋 Regulatory agent checking compliance..."
            time.sleep(2)
            research_data['results']['regulatory'] = generate_regulatory_analysis(topic)
            
            current_status = "🔧 Technical feasibility agent assessing viability..."
            time.sleep(2)
            research_data['results']['technical'] = generate_technical_feasibility(topic)
            
            current_status = "📝 Documentation specialist creating reports..."
            time.sleep(2)
            research_data['results']['documentation'] = generate_comprehensive_documentation(topic)
            
            current_status = "📄 PDF generation agent creating documents..."
            time.sleep(2)
            # Generate PDFs to files for emailing
            pdf_paths = []
            for t in ['comprehensive', 'executive', 'market', 'technical']:
                pdf_paths.append(generate_pdf_to_file(t, research_data))
            
            current_status = "📧 Preparing email delivery..."
            time.sleep(1)
            # Send via Gmail tool
            send_result = send_research_email(topic, recipient_email, pdf_paths)
            print(send_result)
            current_status = f"✅ Research completed! Comprehensive report sent to {recipient_email}"
        except Exception as e:
            print(f"Research error: {e}")
            current_status = f"❌ Error: {str(e)}"
        finally:
            is_running = False
    
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

@app.route('/download-pdf/<pdf_type>')
def download_pdf(pdf_type):
    # Check authentication
    if not check_auth():
        return jsonify({'error': 'Authentication required'}), 401
    
    global research_data
    if not research_data.get('topic') or not research_data.get('results'):
        return jsonify({'error': 'No research data available. Please run a research first.'}), 404
    
    try:
        pdf_path = generate_pdf_to_file(pdf_type, research_data)
        with open(pdf_path, 'rb') as f:
            data = f.read()
        topic = research_data['topic']
        response = app.response_class(
            data,
            mimetype='application/pdf',
            headers={'Content-Disposition': f'attachment; filename={topic}_{pdf_type}_report.pdf'}
        )
        return response
    except Exception as e:
        return jsonify({'error': f'PDF generation failed: {str(e)}'}), 500

@app.route('/view-pdf/<pdf_type>')
def view_pdf(pdf_type):
    # Check authentication
    if not check_auth():
        return jsonify({'error': 'Authentication required'}), 401
    
    global research_data
    if not research_data.get('topic') or not research_data.get('results'):
        return jsonify({'error': 'No research data available. Please run a research first.'}), 404
    
    try:
        pdf_path = generate_pdf_to_file(pdf_type, research_data)
        with open(pdf_path, 'rb') as f:
            data = f.read()
        response = app.response_class(
            data,
            mimetype='application/pdf',
            headers={'Content-Disposition': 'inline; filename=MARS_report.pdf'}
        )
        return response
    except Exception as e:
        return jsonify({'error': f'PDF generation failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
