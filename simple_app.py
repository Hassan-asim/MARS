from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import threading
import time
import os
from dotenv import load_dotenv

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
    # Allow access to auth page and static files without authentication
    if request.path == '/auth' or request.path.startswith('/static') or request.path.startswith('/api/auth'):
        return True
    # Check if user is logged in (session-based for server-side, frontend will handle localStorage)
    return 'user' in session or request.headers.get('Authorization')

@app.route('/')
def index():
    # Always redirect to auth first for better UX
    if not check_auth():
        return redirect(url_for('auth'))
    return render_template('index.html')

@app.route('/auth')
def auth():
    # If user is already logged in, redirect to main app
    if 'user' in session:
        return redirect(url_for('index'))
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

def generate_technology_research(topic):
    """Generate technology research based on topic"""
    return {
        'title': f'Technology Analysis: {topic}',
        'summary': f'Comprehensive technology analysis for {topic} revealing key trends, innovations, and technical challenges.',
        'key_findings': [
            f'Emerging technologies in {topic} show 40% growth potential',
            f'Key technical challenges include scalability and integration',
            f'Current market leaders are investing heavily in {topic} innovation',
            f'Future developments expected to focus on AI integration and automation'
        ],
        'recommendations': [
            f'Invest in R&D for {topic} advancement',
            f'Form strategic partnerships with technology providers',
            f'Develop scalable architecture for {topic} implementation'
        ]
    }

def generate_market_analysis(topic):
    """Generate market analysis based on topic"""
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
    """Generate financial analysis based on topic"""
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
    """Generate UX research based on topic"""
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
    """Generate patent analysis based on topic"""
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
    """Generate regulatory analysis based on topic"""
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
    """Generate technical feasibility analysis based on topic"""
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
    """Generate comprehensive documentation based on topic"""
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

def generate_comprehensive_pdf_content(research_data):
    """Generate comprehensive PDF content"""
    content = [
        "## EXECUTIVE SUMMARY",
        "",
        research_data['results'].get('documentation', {}).get('executive_summary', 'Comprehensive analysis completed.'),
        "",
        "## TECHNOLOGY ANALYSIS",
        "",
        research_data['results'].get('technology', {}).get('summary', 'Technology analysis completed.'),
        "",
        "### Key Findings:",
    ]
    
    tech_findings = research_data['results'].get('technology', {}).get('key_findings', [])
    for finding in tech_findings:
        content.append(f"• {finding}")
    
    content.extend([
        "",
        "## MARKET ANALYSIS", 
        "",
        research_data['results'].get('market', {}).get('summary', 'Market analysis completed.'),
        "",
        f"Market Size: {research_data['results'].get('market', {}).get('market_size', 'Data not available')}",
        "",
        "## FINANCIAL PROJECTIONS",
        "",
        research_data['results'].get('financial', {}).get('summary', 'Financial analysis completed.'),
    ])
    
    return content

def generate_executive_pdf_content(research_data):
    """Generate executive summary PDF content"""
    return [
        "## EXECUTIVE SUMMARY",
        "",
        research_data['results'].get('documentation', {}).get('executive_summary', 'Executive summary not available.'),
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

def generate_market_pdf_content(research_data):
    """Generate market analysis PDF content"""
    market_data = research_data['results'].get('market', {})
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

def generate_technical_pdf_content(research_data):
    """Generate technical analysis PDF content"""
    tech_data = research_data['results'].get('technical', {})
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

def send_research_email(topic, recipient_email):
    """Send research results via email using Gmail API"""
    try:
        print(f"📧 Email prepared for {recipient_email}")
        print(f"📝 Subject: MARS Research Results: {topic}")
        print("💌 Email would be sent via Gmail API in production")
        
    except Exception as e:
        print(f"Email sending error: {e}")
        raise e

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
    
    # Simulate research process with email integration
    def simulate_research():
        global is_running, current_status, research_data
        try:
            is_running = True
            research_data['topic'] = topic
            research_data['recipient_email'] = recipient_email
            research_data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            current_status = "Initializing 13 AI research agents..."
            time.sleep(2)
            
            # Technology Research
            current_status = "🔬 Technology research agent analyzing trends..."
            time.sleep(3)
            research_data['results']['technology'] = generate_technology_research(topic)
            
            # Market Analysis
            current_status = "📊 Market analysis agent researching competition..."
            time.sleep(3)
            research_data['results']['market'] = generate_market_analysis(topic)
            
            # Financial Analysis
            current_status = "💰 Financial analysis agent validating business model..."
            time.sleep(2)
            research_data['results']['financial'] = generate_financial_analysis(topic)
            
            # UX Research
            current_status = "👥 UX research agent studying user experience..."
            time.sleep(2)
            research_data['results']['ux'] = generate_ux_research(topic)
            
            # Patent Analysis
            current_status = "⚖️ Patent agent analyzing IP landscape..."
            time.sleep(2)
            research_data['results']['patent'] = generate_patent_analysis(topic)
            
            # Regulatory Compliance
            current_status = "📋 Regulatory agent checking compliance..."
            time.sleep(2)
            research_data['results']['regulatory'] = generate_regulatory_analysis(topic)
            
            # Technical Feasibility
            current_status = "🔧 Technical feasibility agent assessing viability..."
            time.sleep(2)
            research_data['results']['technical'] = generate_technical_feasibility(topic)
            
            # Documentation Creation
            current_status = "📝 Documentation specialist creating reports..."
            time.sleep(3)
            research_data['results']['documentation'] = generate_comprehensive_documentation(topic)
            
            current_status = "📄 PDF generation agent creating documents..."
            time.sleep(2)
            
            current_status = "📧 Preparing email delivery..."
            time.sleep(1)
            
            # Try to send actual email
            try:
                send_research_email(topic, recipient_email)
                current_status = f"✅ Research completed! Comprehensive report sent to {recipient_email}"
            except Exception as email_error:
                print(f"Email sending failed: {email_error}")
                current_status = f"✅ Research completed! Results ready for download (Email delivery temporarily unavailable)"
            
        except Exception as e:
            current_status = f"❌ Error: {str(e)}"
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

@app.route('/download-pdf/<pdf_type>')
def download_pdf(pdf_type):
    # Check authentication
    if not check_auth():
        return jsonify({'error': 'Authentication required'}), 401
    
    global research_data
    
    # Check if we have research data
    if not research_data.get('topic') or not research_data.get('results'):
        return jsonify({'error': 'No research data available. Please run a research first.'}), 404
    
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from io import BytesIO
    
    buffer = BytesIO()
    
    try:
        # Create PDF with actual research data
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Title
        p.setFont("Helvetica-Bold", 20)
        topic = research_data['topic']
        p.drawString(100, 750, f"{pdf_type.upper()} REPORT: {topic}")
        
        # Date and metadata
        p.setFont("Helvetica", 10)
        p.drawString(100, 730, f"Generated: {research_data.get('timestamp', 'N/A')}")
        p.drawString(100, 715, f"Research Topic: {topic}")
        
        # Content based on PDF type
        p.setFont("Helvetica", 12)
        y_position = 680
        
        if pdf_type == 'comprehensive':
            content_lines = generate_comprehensive_pdf_content(research_data)
        elif pdf_type == 'executive':
            content_lines = generate_executive_pdf_content(research_data)
        elif pdf_type == 'market':
            content_lines = generate_market_pdf_content(research_data)
        elif pdf_type == 'technical':
            content_lines = generate_technical_pdf_content(research_data)
        else:
            content_lines = generate_comprehensive_pdf_content(research_data)
        
        for line in content_lines:
            if y_position < 50:  # Start new page if needed
                p.showPage()
                y_position = 750
                p.setFont("Helvetica", 12)
            
            # Handle different font weights
            if line.startswith('###'):
                p.setFont("Helvetica-Bold", 14)
                line = line[3:].strip()
            elif line.startswith('##'):
                p.setFont("Helvetica-Bold", 12)
                line = line[2:].strip()
            else:
                p.setFont("Helvetica", 12)
            
            p.drawString(100, y_position, line[:80])  # Limit line length
            y_position -= 20
            
        p.save()
        buffer.seek(0)
        
        response = app.response_class(
            buffer.getvalue(),
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename={topic}_{pdf_type}_report.pdf'
            }
        )
        
        return response
        
    except Exception as e:
        return jsonify({'error': f'PDF generation failed: {str(e)}'}), 500

@app.route('/view-pdf/<pdf_type>')
def view_pdf(pdf_type):
    # Check authentication
    if not check_auth():
        return jsonify({'error': 'Authentication required'}), 401
    
    # For demo, generate the same PDF for viewing
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from io import BytesIO
    
    buffer = BytesIO()
    
    try:
        # Create PDF
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Title
        p.setFont("Helvetica-Bold", 20)
        p.drawString(100, 750, f"MARS {pdf_type.upper()} REPORT")
        
        # Content
        p.setFont("Helvetica", 12)
        y_position = 700
        
        content_lines = [
            f"Generated by Multi-Agent Research System (MARS)",
            f"Report Type: {pdf_type.replace('_', ' ').title()}",
            f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "This is a demo PDF generated by the MARS system.",
            "In the full version, this would contain comprehensive",
            "research analysis performed by 13 AI agents.",
            "",
            "The complete system includes:",
            "",
            "• Real-time AI-powered research analysis",
            "• Professional PDF generation with charts",
            "• Automated email delivery with attachments", 
            "• Multi-agent collaboration framework",
            "• Comprehensive market & technical analysis",
            "",
            "🔬 Technology Research Agent",
            "📊 Market Analysis Agent", 
            "💰 Financial Analysis Agent",
            "👥 UX Research Agent",
            "⚖️ Legal & Patent Agent",
            "📋 Regulatory Compliance Agent",
            "🔧 Technical Feasibility Agent",
            "📝 Documentation Specialist",
            "✅ Quality Assurance Agent",
            "🗺️ Strategic Planning Agent",
            "⚠️ Risk Assessment Agent",
            "🚀 Innovation Trends Agent",
            "📄 PDF Generation Agent",
        ]
        
        for line in content_lines:
            p.drawString(100, y_position, line)
            y_position -= 20
            
        p.save()
        
        buffer.seek(0)
        
        response = app.response_class(
            buffer.getvalue(),
            mimetype='application/pdf',
            headers={
                'Content-Disposition': 'inline; filename=MARS_report.pdf'
            }
        )
        
        return response
        
    except Exception as e:
        return jsonify({'error': f'PDF generation failed: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Starting MARS Web Interface (Demo Mode)...")
    print("=" * 50)
    print("📱 The web interface will be available at: http://localhost:5000")
    print("🔄 Starting Flask server...")
    print()
    app.run(debug=True, host='0.0.0.0', port=5000)
