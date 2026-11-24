from django.test import TestCase

# Create your tests here.
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import tempfile
import os
@login_required
def pdfsview(request, subject):
    temp_files = []  # Track temporary files for cleanup
    try:
        subject_instance = Subject.objects.get(name=subject)

        # Fetch all model instances
        courseoutline = CourseOutline.objects.get(teacher=request.user, subject_name=subject_instance)
        courseobjective = CourseObjective.objects.get(teacher=request.user, subject_name=subject_instance)
        weeklyplan = WeeklyPlan.objects.get(teacher=request.user, subject_name=subject_instance)
        timetable = Timetable.objects.get(teacher=request.user, subject_name=subject_instance)
        attendance_record = AttendanceRecord.objects.get(teacher=request.user, subject_name=subject_instance)
        counselinghours = CounselingHours.objects.get(teacher=request.user, subject_name=subject_instance)
        lecture_notes = LectureNotes.objects.get(teacher=request.user, subject_name=subject_instance)
        reference_material = ReferenceMaterial.objects.get(teacher=request.user, subject_name=subject_instance)
        
        # Fetch presentations
        presentations = Presentation.objects.filter(
            teacher=request.user, 
            subject_name=subject_instance
        )
        
        midterm = MidTermPaper.objects.get(teacher=request.user, subject_name=subject_instance)
        finalterm = FinalTermPaper.objects.get(teacher=request.user, subject_name=subject_instance)
        sessional_marks = SessionalMarks.objects.get(teacher=request.user, subject_name=subject_instance)
        recommendations_suggestions = RecommendationsAndSuggestions.objects.get(
            teacher=request.user, 
            subject_name=subject_instance
        )

        files = []

        # Helper to create presentation PDF table
        def create_presentation_table(presentations):
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title = Paragraph("Presentation Records", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 12))
            
            # Table data
            data = [["Group", "Topic", "Student", "Marks", "Comments"]]
            for pres in presentations:
                comments = pres.comments[:100] + '...' if len(pres.comments) > 100 else pres.comments
                data.append([
                    pres.group_name,
                    pres.topic,
                    pres.student_name,
                    str(pres.marks_obtained),
                    comments
                ])
            
            # Create table
            table = Table(data, colWidths=[80, 120, 80, 50, 150])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4CAF50')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 10),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#E8F5E9')),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
                ('WORDWRAP', (0,0), (-1,-1), 'ON')
            ]))
            elements.append(table)
            doc.build(elements)
            
            pdf_content = buffer.getvalue()
            buffer.close()
            return pdf_content

        # Generate presentation table if presentations exist
        if presentations.exists():
            pres_pdf = create_presentation_table(presentations)
            pres_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            pres_temp.write(pres_pdf)
            pres_temp.close()
            files.append(pres_temp.name)
            temp_files.append(pres_temp.name)

        # Process other sections
        def process_section(content, file_field):
            if content:
                temp_path = create_text_pdf(content)  # Assumes this returns file path
                files.append(temp_path)
                temp_files.append(temp_path)
            elif file_field and file_field.path and os.path.exists(file_field.path):
                temp_path = convert_to_pdf(file_field.path)  # Assumes this returns file path
                files.append(temp_path)
                temp_files.append(temp_path)

        # Add sections in order
        process_section(courseoutline.outline_text, courseoutline.outlinefile)
        process_section(courseobjective.objectives, courseobjective.objectivefile)
        process_section(weeklyplan.weeklyplantopic, weeklyplan.weeklyplanfile)
        process_section(None, timetable.timetablefile)
        process_section(None, attendance_record.attendancerecordfile)
        process_section(counselinghours.counselinghourtopic, counselinghours.counselinghourfile)
        process_section(lecture_notes.lecturenotes, lecture_notes.lecturenotesfile)
        process_section(reference_material.reference_text, reference_material.referencefile)
        process_section(None, midterm.mid_paper_file)
        process_section(None, finalterm.final_paper_file)
        process_section(None, sessional_marks.sessional_marks_file)
        process_section(
            recommendations_suggestions.recommendations, 
            recommendations_suggestions.recommendationsandsuggestionsfile
        )

        if not files:
            return HttpResponse("No data available", status=204)

        # Merge all PDFs
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as output_pdf:
            merge_files_to_pdf(files, output_pdf.name)
            with open(output_pdf.name, 'rb') as f:
                pdf_content = f.read()
            temp_files.append(output_pdf.name)

        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{subject}_materials.pdf"'
        return response

    except Subject.DoesNotExist:
        return HttpResponse("Subject not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
    finally:
        # Cleanup temporary files
        for path in temp_files:
            try:
                os.unlink(path)
            except:
                pass
