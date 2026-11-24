from django import forms
from .models import *
class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = TeacherProfile
        fields = '__all__'
        exclude = ['unread_message_count']  # Exclude non-editable fields

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # pull user from view
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email
            self.user = user  # save user for later use

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            # update user's email as well
            if hasattr(self, 'user'):
                self.user.email = self.cleaned_data['email']
                self.user.save()
        return profile


class TeacherdocumentForm(forms.ModelForm):
    class Meta:
        model=TeacherDocument
        fields='__all__'

class AcademicScheduleForm(forms.ModelForm):
    class Meta:
        model = AcademicSchedule
        fields = ['semester_type', 'year',]
        widgets = {
            'semester_type': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
        }

class CourseObjectiveForm(forms.ModelForm):
    class Meta:
        model = CourseObjective
        fields = [ 'objectives','objectivefile']
        widgets = {
            'objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
                        'objectivefile': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.png,.jpg,.jpeg'})

        }
        required = {
            'outline_text': False,
            'outlinefile': False
        }

class CourseOutlineForm(forms.ModelForm):
    class Meta:
        model = CourseOutline
        fields = ['outline_text', 'outlinefile']
        widgets = {
            'outline_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'outlinefile': forms.FileInput(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super(CourseOutlineForm, self).__init__(*args, **kwargs)
        self.fields['outline_text'].required = False
        self.fields['outlinefile'].required = False



class WeeklyPlanForm(forms.ModelForm):
    class Meta:
        model = WeeklyPlan
        fields = [ 'weeklyplantopic','weeklyplanfile']
        widgets = {
            'weeklyplantopic': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'weeklyplanfile':forms.FileInput(attrs={'class': 'form-control'})

        }

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = [ 'timetablefile']
        widgets = {
        
            'timetablefile': forms.FileInput(attrs={'class': 'form-control'})
        }

class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = [ 'attendancerecordfile']
        widgets = {
            
            'attendancerecordfile': forms.FileInput(attrs={'class': 'form-control'})
        }

class MakeupClassForm(forms.ModelForm):
    class Meta:
        model = MakeupClass
        
        fields = [ 'makeupclasstopic','makeupclassfile']
        widgets = {
            'makeupclasstopic': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'makeupclassfile':forms.FileInput(attrs={'class': 'form-control'})

        }

class CounselingHoursForm(forms.ModelForm):
    class Meta:
        model = CounselingHours
           
        fields = [ 'counselinghourtopic','counselinghourfile']
        widgets = {
            'counselinghourtopic': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'counselinghourfile':forms.FileInput(attrs={'class': 'form-control'})

        }

class LectureNotesForm(forms.ModelForm):
    class Meta:
        model = LectureNotes
        fields = [ 'lecturenotes','lecturenotesfile']
        widgets = {
            'lecturenotes':forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'lecturenotesfile': forms.FileInput(attrs={'class': 'form-control'})
        }

class ReferenceMaterialForm(forms.ModelForm):
    class Meta:
        model = ReferenceMaterial
        fields = [ 'reference_text','referencefile']
        widgets = {
            'reference_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
                        'referencefile': forms.FileInput(attrs={'class': 'form-control'})

        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [ 'assignment_number', 'category', 'file', 'marks_obtained', 'comments']
        widgets = {
            'assignment_number': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = [ 'quiz_number', 'category', 'file', 'marks_obtained', 'comments']
        widgets = {
            'quiz_number': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }

class PresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = [ 'group_name', 'topic', 'student_name', 'marks_obtained', 'comments']
        widgets = {
            'group_name': forms.TextInput(attrs={'class': 'form-control'}),
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'student_name': forms.TextInput(attrs={'class': 'form-control'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }

class MidTermPaperForm(forms.ModelForm):
    class Meta:
        model = MidTermPaper
        fields = [ 'mid_paper_file', 'mid_solution_file']
        widgets = {
            'mid_paper_file': forms.FileInput(attrs={'class': 'form-control'}),
                        'mid_solution_file': forms.FileInput(attrs={'class': 'form-control'})

        }

class FinalTermPaperForm(forms.ModelForm):
    class Meta:
        model = FinalTermPaper
        fields = [ 'final_paper_file','final_solution_file' ]
        widgets = {
            'final_paper_file': forms.FileInput(attrs={'class': 'form-control'}),
                        'final_solution_file': forms.FileInput(attrs={'class': 'form-control'})

        }

class SessionalMarksForm(forms.ModelForm):
    class Meta:
        model = SessionalMarks
        fields = [ 'sessional_marks_file']
        widgets = {
            'sessional_marks_file': forms.FileInput(attrs={'class': 'form-control'})
        }

class RecommendationsAndSuggestionsForm(forms.ModelForm):
    class Meta:
        model = RecommendationsAndSuggestions
        fields = ['recommendations','recommendationsandsuggestionsfile']
        widgets = {
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'recommendationsandsuggestionsfile':forms.FileInput(attrs={'class': 'form-control'})
        }