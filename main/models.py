
# models.py
from django.db import models

from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure unique subject names

    def __str__(self):
        return self.name

class Year(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure unique year names

    def __str__(self):
        return self.name

class SemesterType(models.Model):  # Fixed naming convention (PascalCase)
    name = models.CharField(max_length=100, unique=True)  # Ensure unique semester types

    def __str__(self):
        return self.name

class TeacherProfile(models.Model):

    name=models.CharField(blank=True,max_length=100)
    PERMANENT = 'Permanent'
    VISITING = 'Visiting'

    STATUS_CHOICES = [
        (PERMANENT, 'Permanent'),
        (VISITING, 'Visiting'),
    ]
    
    # Use the choices in the field definition
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PERMANENT, 
         blank=True # Default to 'Permanent'
    )

    designation = models.CharField(max_length=100, blank=True)
    faculty_type=models.CharField(max_length=100,blank=True,        choices=STATUS_CHOICES,)

    employe_id=models.CharField(max_length=100,blank=True)

    department_from=models.CharField(max_length=100,blank=True)
    program=models.CharField(max_length=100,blank=True)
    FALL = 'Fall'
    SPRING = 'Spring'
    SUMMER = 'Summer'

    SEMESTER_CHOICES = [
        (FALL, 'Fall'),
        (SPRING, 'Spring'),
        (SUMMER, 'Summer'),
    ]

    semester_type = models.CharField(
        max_length=10,
        choices=SEMESTER_CHOICES,
        default=FALL,
          blank=True  # Set default to Fall
    )
    THEORY = 'THEORY'
    LAB = 'LAB'
    
    SUBJECT_TYPE_CHOICES = [
        (THEORY, 'Theory'),
        (LAB, 'Lab'),
    ]
    
    subject_type = models.CharField(
        max_length=23,
        choices=SUBJECT_TYPE_CHOICES,
        default=THEORY,
        blank=True
    )


    semester_year = models.IntegerField(
        null=True,
        blank=True,
        choices=[(year, year) for year in range(2022, 2030)]  # Predefined years range
    )
    classname=models.CharField(null=True, max_length=50,blank=True)
    semester=models.CharField(null=True, max_length=50,blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True)  
    experience = models.FloatField(null=True,blank=True)
    grade = models.IntegerField(null=True,blank=True)
    section = models.CharField(max_length=50,null=True,blank=True)
    cell_no = models.CharField(max_length=20,null=True,blank=True)
    bio = models.TextField(blank=True, null=True)  # A short biography of the teache
    profile_picture = models.ImageField(upload_to='teacher_pics/', blank=True, null=True) 
    first_login=models.BooleanField(default=True)
    # In your TeacherProfile model
    unread_message_count = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"{self.user.username}'s Profile"


class AcademicSchedule(models.Model):
    
    
    semester_type = models.ForeignKey(SemesterType, on_delete=models.CASCADE, related_name='academic_schedules')
    year=models.ForeignKey(Year, on_delete=models.CASCADE, related_name='academic_schedules')
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='academic_schedules',blank=True,null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_academic_schedules')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.subject_name} - {self.semester_type.name} {self.year.name} Schedule by {self.teacher.username}"


class CourseObjective(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_objectives')
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='course_objectives',blank=True,null=True)
    objectives = models.TextField()  # Teacher writes objectives
    objectivefile = models.FileField(upload_to='documents/course_objectives/', blank=True, null=True)  # Optional file upload

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject_name} - Objectives by {self.teacher.username}"

class CourseOutline(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_outlines')
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='course_outlines',blank=True,null=True)
    outline_text = models.TextField(blank=True, null=True)  # Optional text-based outline
    outlinefile = models.FileField(upload_to='documents/course_outlines/', blank=True, null=True)  # Optional file upload
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject_name} - Outline by {self.teacher.username}"



class WeeklyPlan(models.Model):

    weeklyplantopic = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE,blank=True,null=True)
    weeklyplanfile= models.FileField(upload_to='documents/weeklyplanfile/', help_text="Upload an Excel file (.xlsx) with the weeklyPlan")
    
    def __str__(self):
        return f"{self.subject_name} - Week {self.weeklyplantopic}"
class Timetable(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timetables')
    timetablefile = models.FileField(upload_to='documents/timetables/', help_text="Upload an Excel file (.xlsx) with the timetable")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetables')

    def __str__(self):
        return f"{self.subject_name} - Timetable by {self.teacher.username}"
class AttendanceRecord(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='attendance_records',blank=True,null=True)
    attendancerecordfile = models.FileField(upload_to='documents/attendance/', help_text="Upload an Excel file (.xlsx) with attendance")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject_name} - Attendance by {self.teacher.username}"


class MakeupClass(models.Model):
    makeupclasstopic = models.TextField( blank=True, null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE,blank=True,null=True)
    makeupclassfile= models.FileField(upload_to='documents/makeupclassfile/',  blank=True, null=True,help_text="Upload an Excel file (.xlsx) with the MakeupClass")
    
    def __str__(self):
        return f"{self.subject_name}"



class CounselingHours(models.Model):
    counselinghourtopic = models.TextField(blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE,blank=True,null=True)
    counselinghourfile= models.FileField(upload_to='documents/counselinghourfile/', help_text="Upload an Excel file (.xlsx) with the counselinghour")
    
    def __str__(self):
        return f"{self.teacher.username} - Counseling Hours for {self.subject_name}"

class LectureNotes(models.Model):
    lecturenotes = models.TextField(help_text="Enter books, research papers, or links used as references.",blank=True,null=True)

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lecture_notes')
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lecture_notes',blank=True,null=True)
    lecturenotesfile = models.FileField(upload_to='documents/lecture_notes/', help_text="Upload lecture materials (PDF, PPT, DOCX)")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject_name} - Lecture Notes by {self.teacher.username}"
class ReferenceMaterial(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reference_materials')
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='reference_materials',blank=True,null=True)
    reference_text = models.TextField(
    null=True, 
    blank=True,
    help_text="Enter books, research papers, or links used as references."
    )

    referencefile = models.FileField(
    upload_to='documents/reference_maeterial/', 
    null=True, 
    blank=True,
    help_text="Upload reference materials (PDF, PPT, DOCX)"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject_name} - Reference by {self.teacher.username}"
    
class Assignment(models.Model):
    BEST = 'Best'
    AVERAGE = 'Average'
    WORST = 'Worst'

    CATEGORY_CHOICES = [
        (BEST, 'Best'),
        (AVERAGE, 'Average'),
        (WORST, 'Worst'),
    ]

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments',blank=True,null=True)
    assignment_number = models.PositiveSmallIntegerField(choices=[(i, f"Assignment {i}") for i in range(1, 4)])
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    file = models.FileField(upload_to='documents/assignments/', help_text="Upload marked student assignments.")
    marks_obtained = models.PositiveSmallIntegerField(help_text="Marks out of 10")
    comments = models.TextField(help_text="Provide at least three comments based on rubric")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject_name} - {self.assignment_number} ({self.category}) by {self.teacher.username}"

class Quiz(models.Model):
    BEST = 'Best'
    AVERAGE = 'Average'
    WORST = 'Worst'

    CATEGORY_CHOICES = [
        (BEST, 'Best'),
        (AVERAGE, 'Average'),
        (WORST, 'Worst'),
    ]

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes',blank=True,null=True)
    quiz_number = models.PositiveSmallIntegerField(choices=[(i, f"Quiz {i}") for i in range(1, 4)])
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    file = models.FileField(upload_to='documents/quizzes/', help_text="Upload marked quizzes.")
    marks_obtained = models.PositiveSmallIntegerField(help_text="Marks out of 10")
    comments = models.TextField(help_text="Provide at least three comments based on rubric")
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.subject_name} - {self.quiz_number} ({self.category}) by {self.teacher.username}"

class QuizMarks(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_marks')
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quiz_marks',blank=True,null=True)
    quiz=models.OneToOneField(Quiz, on_delete=models.CASCADE, null=True, blank=True)
class AssigmentMarks(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignment_marks')
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignment_marks',blank=True,null=True)
    assignment=models.OneToOneField(Assignment, on_delete=models.CASCADE, null=True, blank=True)

class Presentation(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='presentations')
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='presentations',blank=True,null=True)
    group_name = models.CharField(max_length=100)
    topic = models.CharField(max_length=200)
    student_name = models.CharField(max_length=100)
    marks_obtained = models.PositiveSmallIntegerField(help_text="Marks out of 10")
    comments = models.TextField(help_text="Teacher's feedback")

    def __str__(self):
        return f"{self.subject_name} - {self.group_name} ({self.topic})"
class MidTermPaper(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mid_term_papers')
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='mid_term_papers', blank=True, null=True)
    mid_paper_file = models.FileField(upload_to='documents/mid_term_paper/', help_text="Upload Mid-term Paper")
    mid_solution_file = models.FileField(upload_to='documents/mid_term_solution/', help_text="Upload Mid-term Solution")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.username} - {self.subject_name.name}"

class MidTermSolution(models.Model):
    BEST = 'Best'
    AVERAGE = 'Average'
    WORST = 'Worst'

    CATEGORY_CHOICES = [
        (BEST, 'Best'),
        (AVERAGE, 'Average'),
        (WORST, 'Worst'),
    ]

    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='mid_term_paper',blank=True,null=True)
    

    mid_term_paper = models.ForeignKey(MidTermPaper, on_delete=models.CASCADE, related_name='solutions')
    solution_number = models.PositiveSmallIntegerField(choices=[(i, f"Solution {i}") for i in range(1, 4)])
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    marks_obtained = models.PositiveSmallIntegerField(help_text="Marks out of 10")
    
    solution_file = models.FileField(upload_to='documents/mid_term_solutions/', help_text="Upload Mid-term Solution")
    comments = models.TextField(blank=True, help_text="Optional comments")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mid_term_paper', 'solution_number')  # Ensure no duplicates

    def __str__(self):
        return f"{self.mid_term_paper} - Solution {self.solution_number}"

# models.py
class FinalTermPaper(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='final_term_paper_uploads')
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='final_term_paper_uploads', blank=True, null=True)
    final_paper_file = models.FileField(upload_to='documents/final_term_paper/', help_text="Upload Final Term Paper")
    final_solution_file = models.FileField(upload_to='documents/final_term_solution/', help_text="Upload Final Term Solution")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject_name} - Final Term Paper by {self.teacher.username}"


class FinalTermSolution(models.Model):
    BEST = 'Best'
    AVERAGE = 'Average'
    WORST = 'Worst'

    CATEGORY_CHOICES = [
        (BEST, 'Best'),
        (AVERAGE, 'Average'),
        (WORST, 'Worst'),
    ]

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='final_term_solution_uploads')
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='final_term_solution_uploads', blank=True, null=True)

    final_term_paper = models.ForeignKey(FinalTermPaper, on_delete=models.CASCADE, related_name='solutions')
    solution_number = models.PositiveSmallIntegerField(choices=[(i, f"Solution {i}") for i in range(1, 4)])
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    marks_obtained = models.PositiveSmallIntegerField(help_text="Marks out of 10")
    
    solution_file = models.FileField(upload_to='documents/final_term_solution/', help_text="Upload Final Term Solution")
    comments = models.TextField(blank=True, help_text="Optional comments")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('final_term_paper', 'solution_number')  # Prevent duplicate solution numbers per paper

    def __str__(self):
        return f"{self.final_term_paper.subject_name} - Solution {self.solution_number}"


class SessionalMarks(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='sessional_marks',blank=True,null=True)
    sessional_marks_file = models.FileField(upload_to='documents/sessional_marks/', help_text="Upload Sessional Marks Excel file")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject_name} - Sessional Marks by {self.teacher.username}"
class RecommendationsAndSuggestions(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='recommendationsandsuggestions',blank=True,null=True)
    recommendations = models.TextField(help_text="Write your recommendations and suggestions")
    created_at = models.DateTimeField(auto_now_add=True)
    recommendationsandsuggestionsfile = models.FileField(upload_to='documents/recommendationsandsuggestions/', help_text="Upload recommendationsandsuggestionsfile (PDF, PPT, DOCX)")

    def __str__(self):
        return f"Recommendations for {self.subject_name} by {self.teacher.username}"






class TeacherDocument(models.Model):
    user = models.ForeignKey(User,null=True ,on_delete=models.CASCADE,blank=True)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, )
    academic_schedule = models.OneToOneField(AcademicSchedule, on_delete=models.CASCADE, null=True, blank=True)

    course_objective = models.OneToOneField(CourseObjective, on_delete=models.CASCADE, null=True, blank=True)
    course_outline = models.OneToOneField(CourseOutline, on_delete=models.CASCADE, null=True, blank=True)
    weekly_plan = models.OneToOneField(WeeklyPlan, on_delete=models.CASCADE, null=True, blank=True)
    timetable = models.OneToOneField(Timetable, on_delete=models.CASCADE, null=True, blank=True)
    attendance_record = models.OneToOneField(AttendanceRecord, on_delete=models.CASCADE, null=True, blank=True)
    record_of_makeup_classes = models.OneToOneField(MakeupClass, on_delete=models.CASCADE, null=True, blank=True)
    counseling_hours = models.OneToOneField(CounselingHours, on_delete=models.CASCADE, null=True, blank=True)
    lecture_notes = models.OneToOneField(LectureNotes, on_delete=models.CASCADE, null=True, blank=True)
    reference_materials = models.OneToOneField(ReferenceMaterial, on_delete=models.CASCADE, null=True, blank=True)
    assignments = models.ManyToManyField(Assignment, blank=True, related_name='teacher_documents')

    quizzes = models.ManyToManyField(Quiz, blank=True, related_name='teacher_documents')
    presentations = models.ManyToManyField(Presentation, null=True, blank=True)
    mid_term_paper = models.OneToOneField(MidTermPaper, on_delete=models.CASCADE, null=True, blank=True)
    final_term_paper = models.OneToOneField(FinalTermPaper, on_delete=models.CASCADE, null=True, blank=True)
    sessional_marks = models.OneToOneField(SessionalMarks, on_delete=models.CASCADE, null=True, blank=True)
    recommendations_suggestions = models.OneToOneField(RecommendationsAndSuggestions,on_delete=models.CASCADE,null=True,blank=True) # Storing text-based suggestions
    color = models.CharField(max_length=7, default="#000000")  # HEX color format

    APPROVED = 'approved'
    PENDING = 'pending'
    REJECTED = 'rejected'
    ASSIGN='assign'
    
    STATUS_CHOICES = [
        (ASSIGN, 'Assign'),
        (APPROVED, 'Approved'),  # Approved status
        (PENDING, 'Pending'),    # Pending status
        (REJECTED, 'Rejected'),  # Rejected status
    ]
    
    status = models.CharField(
        max_length=10,           
        choices=STATUS_CHOICES,  
        default=PENDING,
        null=True     
    )
    
    comment = models.TextField(
        blank=True,   
        null=True     
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()}"








class SubjectComment(models.Model):
    teacher_document = models.ForeignKey(TeacherDocument, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notified = models.BooleanField(default=False)  # Add this field

    def __str__(self):
        return f"Comment on {self.teacher_document} by {self.teacher_document.user.username}"




# models.py

# models.py

from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Notification for {self.user.username}'





from django.contrib.auth.models import User
from django.db import models

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # New field


    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:30]}"
 










