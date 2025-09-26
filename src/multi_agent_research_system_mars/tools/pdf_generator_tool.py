import os
import tempfile
from typing import Type, Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from datetime import datetime
import markdown
import pdfkit
from jinja2 import Template


class PDFGeneratorToolInput(BaseModel):
    """Input schema for PDF Generator tool."""
    content: str = Field(..., description="Markdown content to convert to PDF")
    title: str = Field(..., description="Document title")
    filename: str = Field(..., description="Output PDF filename")
    document_type: str = Field(default="report", description="Type of document (report, executive_summary, etc.)")


class PDFGeneratorTool(BaseTool):
    name: str = "PDF Document Generator"
    description: str = (
        "Convert markdown content to professionally formatted PDF documents. "
        "Creates high-quality PDFs with proper headers, footers, table of contents, "
        "and corporate-standard formatting suitable for business presentations."
    )
    args_schema: Type[BaseModel] = PDFGeneratorToolInput

    def __init__(self):
        super().__init__()
        # Create output directory if it doesn't exist
        self.output_dir = os.path.join(os.getcwd(), "generated_pdfs")
        os.makedirs(self.output_dir, exist_ok=True)

    def _create_html_template(self, content: str, title: str, document_type: str) -> str:
        """Create HTML template with professional styling."""
        
        # Convert markdown to HTML
        md_content = markdown.markdown(content, extensions=['tables', 'fenced_code', 'toc'])
        
        # Professional HTML template
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ title }}</title>
            <style>
                @page {
                    size: A4;
                    margin: 1in;
                    @top-center {
                        content: "{{ title }}";
                        font-family: 'Arial', sans-serif;
                        font-size: 10pt;
                        color: #666;
                        border-bottom: 1px solid #ddd;
                        padding-bottom: 5px;
                    }
                    @bottom-center {
                        content: "Page " counter(page) " of " counter(pages);
                        font-family: 'Arial', sans-serif;
                        font-size: 9pt;
                        color: #666;
                    }
                    @bottom-right {
                        content: "Generated on {{ date }}";
                        font-family: 'Arial', sans-serif;
                        font-size: 8pt;
                        color: #999;
                    }
                }
                
                body {
                    font-family: 'Arial', 'Helvetica', sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 100%;
                    margin: 0;
                    padding: 0;
                }
                
                .cover-page {
                    page-break-after: always;
                    text-align: center;
                    padding-top: 200px;
                }
                
                .cover-title {
                    font-size: 36pt;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 30px;
                    line-height: 1.2;
                }
                
                .cover-subtitle {
                    font-size: 18pt;
                    color: #7f8c8d;
                    margin-bottom: 50px;
                }
                
                .cover-info {
                    font-size: 14pt;
                    color: #95a5a6;
                    margin-top: 100px;
                }
                
                h1 {
                    color: #2c3e50;
                    font-size: 24pt;
                    font-weight: bold;
                    margin-top: 30px;
                    margin-bottom: 20px;
                    page-break-before: auto;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                }
                
                h2 {
                    color: #34495e;
                    font-size: 18pt;
                    font-weight: bold;
                    margin-top: 25px;
                    margin-bottom: 15px;
                }
                
                h3 {
                    color: #5d6d7e;
                    font-size: 14pt;
                    font-weight: bold;
                    margin-top: 20px;
                    margin-bottom: 10px;
                }
                
                h4, h5, h6 {
                    color: #85929e;
                    font-size: 12pt;
                    font-weight: bold;
                    margin-top: 15px;
                    margin-bottom: 8px;
                }
                
                p {
                    margin-bottom: 12px;
                    text-align: justify;
                    font-size: 11pt;
                }
                
                ul, ol {
                    margin-bottom: 15px;
                    padding-left: 25px;
                }
                
                li {
                    margin-bottom: 5px;
                    font-size: 11pt;
                }
                
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    font-size: 10pt;
                }
                
                th, td {
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }
                
                th {
                    background-color: #f8f9fa;
                    font-weight: bold;
                    color: #2c3e50;
                }
                
                tr:nth-child(even) {
                    background-color: #f8f9fa;
                }
                
                .executive-summary {
                    background-color: #ecf0f1;
                    border-left: 5px solid #3498db;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 5px;
                }
                
                .highlight {
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 15px 0;
                }
                
                code {
                    background-color: #f8f9fa;
                    padding: 2px 5px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                    font-size: 10pt;
                }
                
                pre {
                    background-color: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 5px;
                    padding: 15px;
                    overflow-x: auto;
                    font-size: 9pt;
                }
                
                blockquote {
                    border-left: 4px solid #3498db;
                    margin-left: 0;
                    padding-left: 20px;
                    font-style: italic;
                    color: #7f8c8d;
                }
                
                .page-break {
                    page-break-before: always;
                }
                
                .no-break {
                    page-break-inside: avoid;
                }
                
                .toc {
                    page-break-after: always;
                }
                
                .toc h2 {
                    color: #2c3e50;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                }
                
                .toc ul {
                    list-style: none;
                    padding-left: 0;
                }
                
                .toc li {
                    margin-bottom: 8px;
                    font-size: 11pt;
                }
                
                .toc a {
                    text-decoration: none;
                    color: #2c3e50;
                }
                
                .footer-info {
                    font-size: 8pt;
                    color: #95a5a6;
                    text-align: center;
                    margin-top: 50px;
                    border-top: 1px solid #ecf0f1;
                    padding-top: 20px;
                }
            </style>
        </head>
        <body>
            <!-- Cover Page -->
            <div class="cover-page">
                <div class="cover-title">{{ title }}</div>
                <div class="cover-subtitle">{{ document_type.replace('_', ' ').title() }}</div>
                <div class="cover-info">
                    <p>Generated by MARS - Multi-Agent Research System</p>
                    <p>{{ date }}</p>
                </div>
            </div>
            
            <!-- Table of Contents would be generated here if needed -->
            
            <!-- Main Content -->
            <div class="content">
                {{ content }}
            </div>
            
            <!-- Footer -->
            <div class="footer-info">
                <p>This document was generated by MARS (Multi-Agent Research System)</p>
                <p>Powered by GLM-4 AI and CrewAI Framework</p>
            </div>
        </body>
        </html>
        """
        
        # Render template
        template = Template(html_template)
        current_date = datetime.now().strftime("%B %d, %Y")
        
        return template.render(
            title=title,
            content=md_content,
            document_type=document_type,
            date=current_date
        )

    def _run(self, content: str, title: str, filename: str, document_type: str = "report") -> str:
        """Generate PDF from markdown content."""
        try:
            # Create HTML from markdown
            html_content = self._create_html_template(content, title, document_type)
            
            # Create temporary HTML file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_html:
                temp_html.write(html_content)
                temp_html_path = temp_html.name
            
            # Output PDF path
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            
            output_path = os.path.join(self.output_dir, filename)
            
            # PDF generation options
            options = {
                'page-size': 'A4',
                'margin-top': '1in',
                'margin-right': '1in',
                'margin-bottom': '1in',
                'margin-left': '1in',
                'encoding': "UTF-8",
                'no-outline': None,
                'enable-local-file-access': None,
                'print-media-type': None,
                'disable-smart-shrinking': None,
            }
            
            try:
                # Generate PDF using wkhtmltopdf
                pdfkit.from_file(temp_html_path, output_path, options=options)
                
                # Clean up temporary file
                os.unlink(temp_html_path)
                
                return f"PDF generated successfully: {output_path}"
                
            except Exception as pdf_error:
                # Fallback: Create a simple text-based PDF if wkhtmltopdf fails
                return self._create_simple_pdf(content, title, filename)
                
        except Exception as e:
            return f"Error generating PDF: {str(e)}"

    def _create_simple_pdf(self, content: str, title: str, filename: str) -> str:
        """Fallback method to create a simple PDF using reportlab."""
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            
            output_path = os.path.join(self.output_dir, filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(output_path, pagesize=A4,
                                  rightMargin=72, leftMargin=72,
                                  topMargin=72, bottomMargin=18)
            
            # Get styles
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=colors.darkblue,
                alignment=1  # Center alignment
            )
            
            # Story (content) list
            story = []
            
            # Add title
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 20))
            
            # Add generation info
            info_text = f"Generated by MARS - Multi-Agent Research System<br/>{datetime.now().strftime('%B %d, %Y')}"
            story.append(Paragraph(info_text, styles['Normal']))
            story.append(PageBreak())
            
            # Process content (simple markdown to text conversion)
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    story.append(Spacer(1, 12))
                elif line.startswith('# '):
                    story.append(Paragraph(line[2:], styles['Heading1']))
                elif line.startswith('## '):
                    story.append(Paragraph(line[3:], styles['Heading2']))
                elif line.startswith('### '):
                    story.append(Paragraph(line[4:], styles['Heading3']))
                else:
                    # Clean up markdown formatting
                    clean_line = line.replace('**', '').replace('*', '').replace('`', '')
                    if clean_line:
                        story.append(Paragraph(clean_line, styles['Normal']))
            
            # Build PDF
            doc.build(story)
            
            return f"Simple PDF generated successfully: {output_path}"
            
        except ImportError:
            # If reportlab is not available, create a text file
            output_path = os.path.join(self.output_dir, filename.replace('.pdf', '.txt'))
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"{title}\n")
                f.write("=" * len(title) + "\n\n")
                f.write(f"Generated by MARS - {datetime.now().strftime('%B %d, %Y')}\n\n")
                f.write(content)
            
            return f"Text file generated (PDF libraries not available): {output_path}"
        
        except Exception as e:
            return f"Error generating simple PDF: {str(e)}"


# Create an instance of the tool for easy import
pdf_generator_tool = PDFGeneratorTool()
