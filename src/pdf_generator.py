from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime


def generate_analysis_pdf(
    summary: str,
    ats_score: str,
    ats_analysis: str,
    gaps: str,
    roadmap: str,
    keywords: str = "",
    jobs: list = None,
    improvements: dict = None
) -> BytesIO:
    """
    Generate a professional PDF report of resume analysis.
    
    Args:
        summary: Resume summary
        ats_score: ATS score (0-100)
        ats_analysis: Full ATS analysis
        gaps: Skills gaps analysis
        roadmap: Career roadmap
        keywords: Job keywords (optional)
        jobs: List of job dictionaries (optional)
        improvements: Before/after improvements (optional)
        
    Returns:
        BytesIO object containing the PDF
    """
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#6b7fd7'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=10,
        leading=16
    )
    
    # Title
    elements.append(Paragraph("🤖 AI Resume Analysis Report", title_style))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                              ParagraphStyle('DateStyle', parent=body_style, alignment=TA_CENTER, fontSize=10)))
    elements.append(Spacer(1, 0.3*inch))
    
    # ATS Score Section
    elements.append(Paragraph("📈 ATS Compatibility Score", heading_style))
    
    # Create ATS score table
    score_data = [[f"ATS SCORE: {ats_score}", "out of 100"]]
    score_table = Table(score_data, colWidths=[3*inch, 2*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (0, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 18),
        ('FONTSIZE', (1, 0), (1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elements.append(score_table)
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph(_clean_text(ats_analysis), body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Resume Summary
    elements.append(Paragraph("📑 Resume Summary", heading_style))
    elements.append(Paragraph(_clean_text(summary), body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Skills Gaps
    elements.append(Paragraph("🛠️ Skills Gaps & Missing Areas", heading_style))
    elements.append(Paragraph(_clean_text(gaps), body_style))
    elements.append(Spacer(1,0.2*inch))
    
    # Career Roadmap
    elements.append(Paragraph("🚀 Career Growth Plan", heading_style))
    elements.append(Paragraph(_clean_text(roadmap), body_style))
    
    # Before/After Improvements (if provided)
    if improvements:
        elements.append(PageBreak())
        elements.append(Paragraph("💡 Resume Improvement Suggestions", heading_style))
        
        elements.append(Paragraph("❌ Current Issues:", 
                                 ParagraphStyle('SubHeading', parent=heading_style, fontSize=13, textColor=colors.HexColor('#c62828'))))
        elements.append(Paragraph(_clean_text(improvements.get('current_issues', '')), body_style))
        elements.append(Spacer(1, 0.15*inch))
        
        elements.append(Paragraph("✅ Suggested Improvements:", 
                                 ParagraphStyle('SubHeading', parent=heading_style, fontSize=13, textColor=colors.HexColor('#2e7d32'))))
        elements.append(Paragraph(_clean_text(improvements.get('suggested_improvements', '')), body_style))
    
    # Job Keywords (if provided)
    if keywords:
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("🎯 Recommended Job Keywords", heading_style))
        elements.append(Paragraph(_clean_text(keywords), body_style))
    
    # Job Recommendations (if provided)
    if jobs and len(jobs) > 0:
        elements.append(PageBreak())
        elements.append(Paragraph("💼 Top Job Recommendations", heading_style))
        
        for i, job in enumerate(jobs[:10], 1):  # Limit to top 10
            job_title = job.get('job_title', job.get('title', 'No Title'))
            job_company = job.get('employer_name', job.get('companyName', 'Unknown Company'))
            job_location = job.get('job_city', job.get('location', ''))
            
            elements.append(Paragraph(f"<b>{i}. {_clean_text(job_title)}</b>", body_style))
            elements.append(Paragraph(f"Company: {_clean_text(job_company)}", 
                                    ParagraphStyle('JobDetail', parent=body_style, fontSize=10, leftIndent=15)))
            elements.append(Paragraph(f"Location: {_clean_text(job_location)}", 
                                    ParagraphStyle('JobDetail', parent=body_style, fontSize=10, leftIndent=15)))
            elements.append(Spacer(1, 0.1*inch))
    
    # Footer
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("_" * 80, body_style))
    elements.append(Paragraph("Generated by AI Job Analyzer - Powered by OpenAI GPT-4o", 
                             ParagraphStyle('Footer', parent=body_style, fontSize=9, alignment=TA_CENTER, textColor=colors.grey)))
    
    # Build PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer


def _clean_text(text: str) -> str:
    """Clean text for PDF generation (remove problematic characters)."""
    if not text:
        return ""
    
    # Replace problematic characters
    text = str(text)
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('\n', '<br/>')
    
    return text
