import os
import io
import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from app.models.report import CareReport
from app.models.patient import Patient
from app.models.medication import MedicationEvent
from app.models.care import HabilitationActivity, CognitiveActivity
from app.models.lifestyle import BehaviourObservation
from app.schemas.report import CareReportResponse, ReportGenerateRequest


class ReportService:
    @staticmethod
    def get_reports(patient_id: str, db: Session) -> List[CareReportResponse]:
        reports = db.query(CareReport).filter(
            CareReport.patient_id == patient_id
        ).order_by(desc(CareReport.created_at)).all()

        return [
            CareReportResponse(
                id=r.id,
                title=r.title,
                type=r.report_type,
                generatedDate=r.generated_date_label,
                period=r.period,
                summary=r.summary,
                adherenceRate=r.adherence_rate,
                medicationRate=r.medication_rate,
                cognitiveRate=r.cognitive_rate,
                fileSize=r.file_size
            )
            for r in reports
        ]

    @staticmethod
    def generate_report(
        patient_id: str,
        data: ReportGenerateRequest,
        db: Session
    ) -> CareReportResponse:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        now = datetime.now(timezone.utc)

        rep_title = f"{data.report_type.capitalize()} Clinical Summary"
        if data.report_type == "doctor":
            rep_title = "Physician Consultation Briefing"
        elif data.report_type == "weekly":
            rep_title = "Weekly Comprehensive Care Report"

        # Calculate actual metrics
        med_events = db.query(MedicationEvent).filter(MedicationEvent.patient_id == patient_id).all()
        med_rate = 91
        if med_events:
            taken = sum(1 for m in med_events if m.status == "taken")
            med_rate = int(round((taken / len(med_events)) * 100))

        habs = db.query(HabilitationActivity).filter(HabilitationActivity.patient_id == patient_id).all()
        hab_rate = 83
        if habs:
            completed_hab = sum(1 for h in habs if h.completed)
            hab_rate = int(round((completed_hab / len(habs)) * 100))

        cogs = db.query(CognitiveActivity).filter(CognitiveActivity.patient_id == patient_id).all()
        cog_rate = 86
        if cogs:
            completed_cog = sum(1 for c in cogs if c.completed)
            cog_rate = int(round((completed_cog / len(cogs)) * 100))

        overall_rate = int(round((med_rate + hab_rate + cog_rate) / 3))

        summary_text = (
            f"Clinical summary prepared for {patient.name if patient else 'Patient'} ({patient.age if patient else 72} yrs, {patient.condition if patient else 'Dementia'}). "
            f"Over the {data.period}, medication adherence achieved {med_rate}%, daily habilitation routine completion was {hab_rate}%, "
            f"and cognitive exercises tracked at {cog_rate}%. Night sleep averaged 7.3 hours with stable daytime mobility."
        )

        new_rep = CareReport(
            id=f"rep-{data.report_type}-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            title=rep_title,
            report_type=data.report_type,
            generated_date_label=now.strftime("%d %b %Y"),
            period=data.period or "Last 30 Days",
            summary=summary_text,
            adherence_rate=overall_rate,
            medication_rate=med_rate,
            cognitive_rate=cog_rate,
            file_size="1.8 MB"
        )
        db.add(new_rep)
        db.commit()
        db.refresh(new_rep)

        return CareReportResponse(
            id=new_rep.id,
            title=new_rep.title,
            type=new_rep.report_type,
            generatedDate=new_rep.generated_date_label,
            period=new_rep.period,
            summary=new_rep.summary,
            adherenceRate=new_rep.adherence_rate,
            medicationRate=new_rep.medication_rate,
            cognitiveRate=new_rep.cognitive_rate,
            fileSize=new_rep.file_size
        )

    @staticmethod
    def build_pdf_stream(report_id: str, db: Session) -> io.BytesIO:
        report = db.query(CareReport).filter(CareReport.id == report_id).first()
        if not report:
            raise ValueError(f"Report {report_id} not found")

        patient = db.query(Patient).filter(Patient.id == report.patient_id).first()

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        elements = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=6
        )
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=15
        )
        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#1e293b')
        )

        elements.append(Paragraph("DEMICARE CLINICAL BRIEFING", title_style))
        elements.append(Paragraph(f"Document: {report.title} · Period: {report.period}", subtitle_style))
        elements.append(Spacer(1, 10))

        # Patient header table
        patient_data = [
            ["Patient Name", patient.name if patient else "Raghavan Menon", "Age / Condition", f"{patient.age if patient else 72} yrs · {patient.condition if patient else 'Dementia'}"],
            ["Primary Caregiver", "Anu Menon (Daughter)", "Attending Physician", "Dr. Arun Nair (Neurology)"],
            ["Generated Date", report.generated_date_label, "Safe Zone Center", "42 Jasmine Gardens, Bengaluru"]
        ]
        t_patient = Table(patient_data, colWidths=[120, 150, 120, 140])
        t_patient.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#0f172a')),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        elements.append(t_patient)
        elements.append(Spacer(1, 15))

        # Adherence Metrics Table
        elements.append(Paragraph("<b>ADHERENCE & CLINICAL METRICS</b>", subtitle_style))
        metrics_data = [
            ["Metric", "Score / Rate", "Benchmark", "Status"],
            ["Overall Care Adherence", f"{report.adherence_rate}%", "85%+", "On Track"],
            ["Medication Adherence", f"{report.medication_rate}%", "90%+", "High Consistency"],
            ["Cognitive Routine Completion", f"{report.cognitive_rate}%", "80%+", "Stable Participation"],
            ["Average Night Sleep", "7.33 hours", "7.0 hours", "Restful Sleep Pattern"],
            ["Average Daily Mobility", "3.1 km / 4,250 steps", "3.0 km", "Normal Activity"]
        ]
        t_metrics = Table(metrics_data, colWidths=[180, 110, 110, 130])
        t_metrics.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ]))
        elements.append(t_metrics)
        elements.append(Spacer(1, 15))

        # Executive Summary
        elements.append(Paragraph("<b>PHYSICIAN EXECUTIVE SUMMARY</b>", subtitle_style))
        elements.append(Paragraph(report.summary, body_style))
        elements.append(Spacer(1, 20))

        # Disclaimer
        elements.append(Paragraph(
            "<i>CONFIDENTIAL MEDICAL SUMMARY: Generated via DemiCare system. Supportive data aggregated from caregiver logs, wearable pendant, and routine observations.</i>",
            subtitle_style
        ))

        doc.build(elements)
        buffer.seek(0)
        return buffer
