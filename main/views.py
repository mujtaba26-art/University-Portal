import json
import tempfile
from django.forms import modelformset_factory
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .forms import *
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def logins(request):
    # If the user is already logged in
    if request.user.is_authenticated:
        if request.user.is_superuser:
            print("User is authenticated and is a superuser")
            return redirect('admin_dashboard')  # Make sure this name exists in your urls.py
        else:
            return redirect('dashboard')  # Make sure this name exists too

    # If it's a POST request (trying to log in)
    if request.method == "POST":
        teacherid = request.POST.get('teacher-id')  # safer than direct indexing
        password = request.POST.get('password')
        if not User.objects.filter(username=teacherid).exists():
            messages.error(request, "User does not exist. Please contact your department coordinator.")
            return redirect('login')


        user = authenticate(request, username=teacherid, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
        else:
            # Optional: add message for login failure
            return redirect('login')

    # GET request - show the login form
    return render(request, 'login.html')

from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TeacherProfile, TeacherDocument

@login_required(login_url='/login/')
def dashboard(request):
    # Get or create the profile if it doesn't exist
    profile, created = TeacherProfile.objects.get_or_create(user=request.user)

    # Handle form submission to update profile
    if request.method == 'POST':
        name = request.POST.get('name')
        designation = request.POST.get('designation')
        status = request.POST.get('status')
        employeid = request.POST.get('employeid')
        facultytype = request.POST.get('facultytype')

        profile.name = name
        profile.designation = designation
        profile.status = status
        profile.employe_id = employeid
        profile.faculty_type = facultytype
        profile.first_login = False  # mark profile as completed
        profile.save()

        return redirect('dashboard')  # Redirect to avoid resubmission

    # Gather stats
    subjects = TeacherDocument.objects.filter(user=request.user)
    total_course = subjects.count()
    pending = subjects.filter(status='pending').count()
    approved = subjects.filter(status='approved').count()
    rejected = subjects.filter(status='rejected').count()

    return render(request, 'dashboard.html', {
        'show_modal': profile.first_login,
        'profile': profile,
        'subjects': subjects,
        'total_course': total_course,
        'total_pending': pending,
        'total_approved': approved,
        'total_rejected': rejected,
    })

# Function to create user and send email with password
def create_user_and_send_email(username, email, password):
    user = User.objects.create_user(username=username, email=email, password=password)
    
    send_mail(
        'Your account has been created',
        f'Hello {username},\nYour account has been created. Your password is: {password}\nPlease login and change your password. websiste:www.coursefolder.com',
        'syedawaisalishah46@gmail.com',
        [email],
        fail_silently=False,
    )
def logouts(request):
    request.session.pop('first_time_login_shown', None)

    logout(request)
    
    return redirect('login')  
# from django.core.exceptions import PermissionDenied

# class EditProfile(UpdateView):
#     model = TeacherProfile
#     form_class = EditProfileForm
#     template_name = 'profile.html'
#     success_url = reverse_lazy('dashboard')


from django.shortcuts import render, redirect
from .forms import EditProfileForm
from .models import TeacherProfile

def edit_teacher_profile(request):
    # Retrieve the current TeacherProfile based on the logged-in user
    teacher_profile = TeacherProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=teacher_profile,user=request.user)
        
        # Manually set the user if it's not already set in the form
        if not form.instance.user:
            form.instance.user = request.user
        
        if form.is_valid():
            form.instance.user = request.user

            form.save()
            messages.success(request, 'Profile updated successfully.')
        
    else:
        form = EditProfileForm(instance=teacher_profile,user=request.user)
    
    return render(request, 'profile.html', {'form': form})


# def profile(request):
#     profiles=TeacherProfile.objects.filter(user=request.user)
#     if request.method=="POST":
#         name = request.POST['name']
#         designation = request.POST['designation']
#         status = request.POST['status']
#         employeid = request.POST['employeid']
#         facultytype = request.POST['facultytype']
#         userimages=request.post['userimage']
#         experience = request.POST['experience']
#         grade = request.POST['grade']
#         section = request.POST['section']
#         cell_no = request.POST['cell_no']
#         # Optionally, check if a profile exists for the user.
#         # For a new profile creation:
#         TeacherProfile.objects.create(
#             name=name,
#             designation=designation,
#             status=status,
#             employe_id=employeid,
#             faculty_type=facultytype,
#             user=request.user
#         )
#         return redirect('profile')  # Adjust the redirect as needed



#     return render(request,'profile.html',{'profile':profiles})

from django.contrib.auth.models import User

def admin_add(request):
    admin_user = request.user
    users = User.objects.exclude(id=admin_user.id)

    for user in users:
        action.send(
            sender=admin_user,
            verb='added a new item',
            target=user,
            description='Check the new item!'
        )
import json
from django.core.files.storage import FileSystemStorage

from django.http import JsonResponse
from .models import *  # Adjust to import your models
from django.shortcuts import render
from django.http import JsonResponse
from .models import *  # import your models

def upload_folder(request, pk, subject):
        try:
            if request.method == "POST":
                print("POST request received")
                

                profile = TeacherProfile.objects.get(user=request.user)
                subject_instance = Subject.objects.get(name=subject)

                teacher_document,created= TeacherDocument.objects.get_or_create(
                    user=request.user, subject_name=subject_instance,
                ) 
                 
                semester_type = request.POST.get("semester_type")
                print('semester_type{}'.format(semester_type))
                year = request.POST.get("year")
                print('year{}'.format(year))
                midtermpapersolutiondata = request.POST.get('midtermpapersolution_data')
                print(midtermpapersolutiondata)
                final_term_data=request.POST.get('final_term_data')
                print(final_term_data)


                weeklyplantopic = request.POST.get("weeklyplantopic")
                print('weeklyplantopic{}'.format(weeklyplantopic))
                weeklyplanfile = request.FILES.get("weeklyplanfile")
                print('weeklyplanfile{}'.format(weeklyplanfile))
                
                makeupclasstopic = request.POST.get("makeupclasstopic")
                print('makeupclasstopic{}'.format(makeupclasstopic))
                
                makeupclassfile = request.FILES.get("makeupclassfile")
                print('makeupclassfile{}'.format(makeupclassfile))
                counselinghourstopic = request.POST.get("counselinghourtopic")
                print(counselinghourstopic)
                counselinghoursfile = request.FILES.get("counselinghourfile")
                print(counselinghoursfile)
                presentation_data = request.POST.get("presentation_data")
                print('presentation_data{}'.format(presentation_data))
                print("Presentation data keys:", request.POST.keys())
                if presentation_data and presentation_data != '[]':
                    presentations = json.loads(presentation_data)
                    for item in presentations:
                        presentation = Presentation.objects.create(
                            teacher=request.user,
                            group_name=item['groupName'],
                            topic=item['topic'],
                            student_name=item['studentName'],
                            marks_obtained=item['marksObtained'],
                            comments=item['comments'],
                            subject_name=subject_instance
                        )
                        teacher_document.presentations.add(presentation)


                objective = request.POST.get("objective")
                print('objective{}'.format(objective))
                objectivefile = request.FILES.get("objectivefile")
                print('objectivefile{}'.format(objectivefile))
                print("FILES keys:", request.FILES.keys())
                outline = request.POST.get("outline_text")
                print('outline{}'.format(outline)) 
                outlinefile = request.FILES.get("outlinefile")

                print('outlinefile{}'.format(outlinefile))
                timetablefile = request.FILES.get("timetablefile")
                print('timetablefile{}'.format(timetablefile))
                attendancerecordfile = request.FILES.get("attendancerecordfile")
                print('attendancerecordfile{}'.format(attendancerecordfile))

                lecturenotes = request.POST.get("lectureNotes")
                print('lecturenotes{}'.format(lecturenotes))
                lecturenotesfile = request.FILES.get("lecturenotesfile")
                print('lecturenotesfile{}'.format(lecturenotesfile))
                
                referencetext = request.POST.get("reference_text")
                print('referencetext{}'.format(referencetext))
                
                
                referencefile = request.FILES.get("referencefile")
                print('referencefile{}'.format(referencefile))
                midPaperFile = request.FILES.get("midPaperFile")
                midSolutionFile = request.FILES.get("midPaperFile")

                
                print('midPaperFile{}'.format(midPaperFile))

                finalPaperFile = request.FILES.get("finalPaperFile")
                finalSolutionFile = request.FILES.get("finalPaperFile")

                print('finalPaperFile{}'.format(finalPaperFile))
                sessionalMarksFile = request.FILES.get("sessionalMarksFile")

                print('sessionalMarksFile{}'.format(sessionalMarksFile))

                recommendations = request.POST.get("recommendations")
                print('recommendations{}'.format(recommendations))
                recommendationsfile = request.FILES.get("recommendationsandsuggestionsfile")
                print('recommendationsfile{}'.format(recommendationsfile))
                courseobjective_form = CourseObjectiveForm(request.POST, request.FILES)
                CourseOutline_Form = CourseOutlineForm(request.POST, request.FILES)
                WeeklyPlan_Form = WeeklyPlanForm(request.POST, request.FILES)
                Timetable_Form = TimetableForm(request.POST, request.FILES)
                AttendanceRecord_Form = AttendanceRecordForm(request.POST, request.FILES)
                MakeupClass_Form = MakeupClassForm(request.POST, request.FILES)
                counseling_form = CounselingHoursForm(request.POST, request.FILES)
                LectureNotes_Form = LectureNotesForm(request.POST, request.FILES)
                ReferenceMaterial_Form = ReferenceMaterialForm(request.POST, request.FILES)
                MidTermPaper_Form = MidTermPaperForm(request.POST, request.FILES)
                FinalTermPaper_Form = FinalTermPaperForm(request.POST, request.FILES)
                SessionalMarks_Form = SessionalMarksForm(request.POST, request.FILES)
                RecommendationsAndSuggestions_Form = RecommendationsAndSuggestionsForm(request.POST, request.FILES)


                # Save associated models
                if semester_type and year:
                    academicschedule = AcademicSchedule.objects.create(
                        teacher=request.user,
                        year=Year.objects.get(name=year),
                        semester_type=SemesterType.objects.get(name=semester_type),
                        subject_name=subject_instance
                    )
                    teacher_document.academic_schedule = academicschedule
                if CourseOutline_Form.is_valid():
                    courseoutlineform=CourseOutline_Form.save(commit=False)
                    courseoutlineform.teacher = request.user
                    courseoutlineform.subject_name = subject_instance
                    courseoutlineform.save()
                    teacher_document.course_outline = courseoutlineform
                if counselinghourstopic or counselinghoursfile:
                    counselinghour=CounselingHours.objects.create(
                        teacher=request.user,
                        subject_name=subject_instance,
                        counselinghourtopic=counselinghourstopic,
                        counselinghourfile=counselinghoursfile,

                    )
                    teacher_document.counseling_hours=counselinghour
                # if counseling_form.is_valid():
                #     counselingHoursform=counseling_form.save(commit=False)
                #     counselingHoursform.teacher = request.user
                #     counselingHoursform.subject_name = subject_instance
                #     counselingHoursform.save()
                #     teacher_document.counseling_hours= counselingHoursform

                if objective or objectivefile:
                    print('objective and objectivefile')
                    courseobjective=CourseObjective.objects.create(
                        teacher=request.user,
                        objectives=objective if objective else "",  
                        objectivefile=objectivefile if objectivefile else "",
                        subject_name=subject_instance
                    )

                    teacher_document.course_objective = courseobjective

                if weeklyplanfile or weeklyplantopic:
                    weeklyplan=WeeklyPlan.objects.create(
                         subject_name=subject_instance,
                         teacher=request.user,
                         weeklyplanfile=weeklyplanfile if weeklyplanfile else "",
                         weeklyplantopic=weeklyplantopic if weeklyplantopic else "",

                    )
                    teacher_document.weekly_plan=weeklyplan
                # if WeeklyPlan_Form.is_valid():
                #     weeklyplanform=WeeklyPlan_Form.save(commit=False)
                #     weeklyplanform.teacher = request.user
                #     weeklyplanform.subject_name = subject_instance
                #     weeklyplanform.save()
                #     teacher_document.weekly_plan = weeklyplanform
                if Timetable_Form.is_valid():
                    timetableform=Timetable_Form.save(commit=False)
                    timetableform.teacher = request.user
                    timetableform.subject_name = subject_instance
                    timetableform.save()
                    teacher_document.timetable = timetableform
                if AttendanceRecord_Form.is_valid():
                    attendancerecordform=AttendanceRecord_Form.save(commit=False)
                    attendancerecordform.teacher = request.user
                    attendancerecordform.subject_name = subject_instance
                    attendancerecordform.save()
                    teacher_document.attendance_record = attendancerecordform
                

                if MakeupClass_Form.is_valid():
                    makeupclassform=MakeupClass_Form.save(commit=False)
                    makeupclassform.teacher = request.user
                    makeupclassform.subject_name = subject_instance
                    makeupclassform.save()
                    teacher_document.record_of_makeup_classes = makeupclassform
                if midPaperFile:
                    midpaperfile=MidTermPaper.objects.create(
                        teacher=request.user,
                        subject_name=subject_instance,
                        mid_paper_file=midPaperFile,
                                                mid_solution_file=midSolutionFile,

                        
  

                    ) 
                    teacher_document.mid_term_paper=midpaperfile
                    if midtermpapersolutiondata:
                        if isinstance(midtermpapersolutiondata, str):
                            solutions = json.loads(midtermpapersolutiondata)
                        else:
                            solutions = midtermpapersolutiondata  # already a Python list

                        for index, item in enumerate(solutions, start=1):
                            MidTermSolution.objects.create(
                                teacher=request.user,
                                subject_name=subject_instance,
                                mid_term_paper=midpaperfile,
                                solution_number=index,  # solution number 1, 2, 3...
                                category=item.get('category', 'Average'),
                                marks_obtained=int(item.get('marks', 0)),
                                solution_file=item.get('file'),  # Ensure this is a valid file object
                                comments=item.get('comments', '')
                            )

                    
                if finalPaperFile:
                    finaltermform=FinalTermPaper.objects.create(
                        teacher=request.user,
                        final_paper_file=finalPaperFile,
                                                final_solution_file=finalSolutionFile,

                        subject_name=subject_instance
                    )
                    teacher_document.final_term_paper=finaltermform
                    if final_term_data:
                        if isinstance(final_term_data, str):
                            solutions = json.loads(final_term_data)
                        else:
                            solutions = final_term_data  # already parsed list

                        for index, item in enumerate(solutions, start=1):
                            FinalTermSolution.objects.create(
                                teacher=request.user,
                                subject_name=subject_instance,
                                final_term_paper=finaltermform,
                                solution_number=index,
                                category=item.get('category', 'Average'),
                                marks_obtained=int(item.get('marks', 0)),
                                solution_file=item.get('file'),  # Ensure this is a file object
                                comments=item.get('comments', '')
                            )

                
                if lecturenotes or lecturenotesfile:
                    lecturenotes=LectureNotes.objects.create(
                        teacher=request.user,
                        lecturenotes=lecturenotes,
                        lecturenotesfile=lecturenotesfile,
                        subject_name=subject_instance
                    )
                    teacher_document.lecture_notes = lecturenotes
                
                if referencetext or referencefile:
                    referencematerial=ReferenceMaterial.objects.create(
                        teacher=request.user,
                        reference_text=referencetext,
                        referencefile=referencefile,
                        subject_name=subject_instance
                    )
                    teacher_document.reference_materials = referencematerial
                
                
                if sessionalMarksFile:
                    sessionalMarksForm=SessionalMarks.objects.create(
                        teacher=request.user,
                        sessional_marks_file=sessionalMarksFile,
                        subject_name=subject_instance
                    )
                    teacher_document.sessional_marks = sessionalMarksForm
                if recommendations or recommendationsfile:
                    recommendationsandsuggestionsform=RecommendationsAndSuggestions.objects.create(
                        teacher=request.user,
                        recommendations=recommendations,
                        recommendationsandsuggestionsfile=recommendationsfile,
                        subject_name=subject_instance
                    )
                    teacher_document.recommendations_suggestions = recommendationsandsuggestionsform
                print(request.FILES.keys())
                for i in range(1, 5):
                    assignment_data = request.POST.get(f'assignment{i}')
                    print(f'Assignment {i} data: {assignment_data}')
                    
                    if assignment_data and assignment_data != '[]':
                        try:
                            assignment_list = json.loads(assignment_data)
                            for item in assignment_list:
                                # Handle file upload
                                file_key = f'assignment{i}file'

                                    
                                # Fix: Access the category directly from item
                                assignment_obj = Assignment.objects.create(
                                    teacher=request.user,
                                    subject_name=subject_instance,
                                    assignment_number=i,
                                    category=item['category'],  # Changed from item.get('assignment{i}Category')
                                    file=file_key,  # Changed from item.get('assignment{i}file')
                                    marks_obtained=item['marks'],  # Changed from item.get('assignment{i}Marks')
                                    comments=item['comments']  # Changed from item.get('assignment{i}Comments')
                                )
                                teacher_document.assignments.add(assignment_obj)
                                print(f"Created assignment: {assignment_obj}")
                        except json.JSONDecodeError as e:
                            print(f'Error decoding JSON for assignment{i}: {str(e)}')
                        except KeyError as e:
                            print(f'Missing key in assignment data: {str(e)}')
                    else:
                        print(f'No assignment{i} data found or empty')
                
                # Process quizzes (similar logic)
                for i in range(1, 5):
                    quiz_data = request.POST.get(f'quiz{i}')
                    print(f'Quiz {i} data: {quiz_data}')
                    
                    if quiz_data and quiz_data != '[]':
                        try:
                            quiz_list = json.loads(quiz_data)

                             
                            for item in quiz_list:
                                    
                                file = item[f'quiz{i}file']
                                # fs = FileSystemStorage()
                                # filename = fs.save(file.name, file)
                                # file_path = fs.url(filename)
                                # print(f'File path for assignment {i}: {file_path}')
                                        
                                # Handle file upload
                                # Fix: Access fields directly from item dictionary
                                quiz_obj = Quiz.objects.create(
                                    teacher=request.user,
                                    subject_name=subject_instance,
                                    quiz_number=i,
                                    category=item[f'quiz{i}Category'],  # Changed from item.get('quiz{i}Category')
                                    file=file,  # Changed from item.get('quiz{i}file')
                                    marks_obtained=item[f'quiz{i}Marks'],  # Changed from item.get('quiz{i}Marks')
                                    comments=item[f'quiz{i}Comments']  # Changed from item.get('quiz{i}Comments')
                                )
                                
                                teacher_document.quizzes.add(quiz_obj)
                                print(f"Created quiz: {quiz_obj}")
                        except json.JSONDecodeError as e:
                            print(f'Error decoding JSON for quiz{i}: {str(e)}')
                        except KeyError as e:
                            print(f'Missing key in quiz data: {str(e)}')
                    else:
                        print(f'No quiz{i} data found or empty')

                
                teacher_document.status = 'pending'
                teacher_document.save()
                # pdfemailsendview(request, subject_instance.name)  # Call the function to send email with PDF

                
                # try:
                # # Generate and email PDF
                #     return JsonResponse({
                #         "success": True, 
                #         "message": "Form submitted and PDF emailed successfully!"
                #     })
                # except Exception as e:
                #     return JsonResponse({
                #         "success": True,
                #         "message": f"Form submitted but PDF email failed: {str(e)}"
                #     })

                     

                return JsonResponse({"success": True, "message": "Form submitted successfully!"})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)


        
        
        else:
        
            semestertypes = SemesterType.objects.all()
            print(semestertypes)
            year=Year.objects.all()  # Fetch all semester types
            
            # If the request is a GET request, create empty forms
            forms_list = {
                
                'course_objective_form': CourseObjectiveForm(),
                'course_outline_form': CourseOutlineForm(),
                'weekly_plan_form': WeeklyPlanForm(),
                'timetable_form': TimetableForm(),
                'attendance_record_form': AttendanceRecordForm(),
                'makeup_class_form': MakeupClassForm(),
                'counseling_hours_form': CounselingHoursForm(),
                'lecture_notes_form': LectureNotesForm(),
                'reference_material_form': ReferenceMaterialForm(),
                'assignment_form': AssignmentForm(),
                'quiz_form': QuizForm(),
                'presentation_form': PresentationForm(),
                'mid_term_paper_form': MidTermPaperForm(),
                'final_term_paper_form': FinalTermPaperForm(),
                'sessional_marks_form': SessionalMarksForm(),
                'recommendations_suggestions_form': RecommendationsAndSuggestionsForm()
            }
            
            context = {'forms': forms_list,'semester_types':semestertypes,
                'year':year,}
        return render(request, 'upload_folder.html', context)






from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import AcademicSchedule, TeacherProfile, Subject, TeacherDocument
from .forms import AcademicScheduleForm
def editupload_folder(request, pk, subject):
    subject_instance = Subject.objects.get(name=subject)
    teacher_document = TeacherDocument.objects.get(user=request.user, subject_name=subject_instance)
    try:
        if request.method == "POST":
            profile = TeacherProfile.objects.get(user=request.user)
            subject = Subject.objects.get(name=subject)

            teacher_document, created = TeacherDocument.objects.get_or_create(
                    user=request.user, subject_name=subject,
                ) 
                 
            semester_type = request.POST.get("semester")
            print('semester_type{}'.format(semester_type))
            year = request.POST.get("year")
            
            objective = request.POST.get("id_objectives")
            print('objective{}'.format(objective))
            objectivefile = request.FILES.get("id_objectivefile")
            
            print('objectivefile{}'.format(objectivefile))
            
            print("FILES keys:", request.FILES.keys())
            print("POST keys:", list(request.POST.keys()))
            outline = request.POST.get("id_outline_text")
            print('outline{}'.format(outline)) 
            outlinefile = request.FILES.get("id_outlinefile")


            print('outlinefile{}'.format(outlinefile))
            weeklyplantopic = request.POST.get("id_weeklyplantopic")
            print('weeklyplantopic{}'.format(weeklyplantopic))
            weeklyplanfile = request.FILES.get("id_weeklyplanfile")
            print('weeklyplanfile{}'.format(weeklyplanfile))
            timetablefile = request.FILES.get("id_timetablefile")
            print('timetablefile{}'.format(timetablefile))
            attendance_record_file = request.FILES.get("id_attendancerecordfile")
            print('attendance_record_file{}'.format(attendance_record_file))
            makeupclasstopic = request.POST.get("id_makeupclasstopic")
            print('makeupclasstopic{}'.format(makeupclasstopic))
            makeupclassfile = request.FILES.get("id_makeupclassfile")
            print('makeupclassfile{}'.format(makeupclassfile))
            counselinghourstopic = request.POST.get("id_counselinghourtopic")
            print('counselinghourstopic{}'.format(counselinghourstopic))
            counselinghoursfile = request.FILES.get("id_counselinghourfile") 
            midTermPapers=request.POST.get("midTermPapers")
            print(midTermPapers)
            
            print('counselinghoursfile{}'.format(counselinghoursfile))
            lecturenotestopic= request.POST.get("id_lecturenotes")
            print('lecturenotestopic{}'.format(lecturenotestopic))
            lecturenotesfile = request.FILES.get("id_lecturenotesfile")
            print('lecturenotesfile{}'.format(lecturenotesfile))
            referencematerialtopic = request.POST.get("id_reference_text")
            print('referencematerialtopic{}'.format(referencematerialtopic))
            referencematerialfile = request.FILES.get("id_referencefile")
            print('referencematerialfile{}'.format(referencematerialfile))
            midPaperFile = request.FILES.get("id_mid_paper_file")
            print('midPaperFile{}'.format(midPaperFile))
            midSolutionFile = request.FILES.get("id_mid_solution_file")
            print('midSolutionFile{}'.format(midSolutionFile))
            finalPaperFile = request.FILES.get("id_final_paper_file")
            print('finalPaperFile{}'.format(finalPaperFile))
            finalSolutionFile = request.FILES.get("id_final_solution_file")
            print('finalSolutionFile{}'.format(finalSolutionFile))
            sessionalMarksFile = request.FILES.get("id_sessional_marks_file")
            print('sessionalMarksFile{}'.format(sessionalMarksFile))
            recommendations = request.POST.get("id_recommendations")
            print('recommendations{}'.format(recommendations))
            recommendationsfile = request.FILES.get("id_recommendationsandsuggestionsfile")
            midtermpapersolutiondata = request.POST.get('midtermpapersolution_data')
            print(midtermpapersolutiondata)
            final_term_data=request.POST.get('final_term_data')
            print(final_term_data)

            
            print('recommendationsfile{}'.format(recommendationsfile))
            assignment1 = request.POST.get("assignment1")
            print('assignment1{}'.format(assignment1))
            assignment2 = request.POST.get("assignment2")
            print('assignment2{}'.format(assignment2))
            assignment3 = request.POST.get("assignment3")
            print('assignment3{}'.format(assignment3))
            assignment4 = request.POST.get("assignment4")
            print('assignment4{}'.format(assignment4))
            quiz1= request.POST.get("quiz1")
            print('quiz1{}'.format(quiz1))
            quiz2= request.POST.get("quiz2")
            print('quiz2{}'.format(quiz2))
            quiz3= request.POST.get("quiz3")
            print('quiz3{}'.format(quiz3))
            quiz4= request.POST.get("quiz4")
            print('quiz4{}'.format(quiz4))

            presentation_data = request.POST.get("presentation_data")
            print('presentation_data{}'.format(presentation_data))

            if presentation_data and presentation_data != '[]':
                presentations = json.loads(presentation_data)
                
                for item in presentations:
                    presentation_id = item.get('id')  # Check if it's an existing record

                    if presentation_id:
                        try:
                            # Try to fetch and update existing Presentation
                            presentation = Presentation.objects.get(id=presentation_id, teacher=request.user)
                            presentation.group_name = item['group_name']
                            presentation.topic = item['topic']
                            presentation.student_name = item['student_name']
                            presentation.marks_obtained = item['marks_obtained']
                            presentation.comments = item['comments']
                            presentation.subject_name = subject_instance
                            presentation.save()
                        except Presentation.DoesNotExist:
                            continue  # Or optionally create a new one if not found
                    else:
                        # Create a new Presentation
                        presentation = Presentation.objects.create(
                            teacher=request.user,
                            group_name=item['group_name'],
                            topic=item['topic'],
                            student_name=item['student_name'],
                            marks_obtained=item['marks_obtained'],
                            comments=item['comments'],
                            subject_name=subject_instance
                        )
                        teacher_document.presentations.add(presentation)

            # Fetch existing instances
            # courseobjective_instance = CourseObjective.objects.get(teacher=request.user, subject_name=subject)
            # print(courseobjective_instance)
            # courseoutline_instance = CourseOutline.objects.get(teacher=request.user, subject_name=subject)
            # weeklyplan_instance = WeeklyPlan.objects.get(teacher=request.user, subject_name=subject)
            # timetable_instance = Timetable.objects.get(teacher=request.user, subject_name=subject)
            # attendancerecord_instance = AttendanceRecord.objects.get(teacher=request.user, subject_name=subject)
            # makeupclass_instance = MakeupClass.objects.get(teacher=request.user, subject_name=subject)
            # counseling_instance = CounselingHours.objects.get(teacher=request.user, subject_name=subject)
            # lecturenotes_instance = LectureNotes.objects.get(teacher=request.user, subject_name=subject)
            # referencematerial_instance = ReferenceMaterial.objects.get(teacher=request.user, subject_name=subject)
            # midterm_instance = MidTermPaper.objects.get(teacher=request.user, subject_name=subject)
            # finalterm_instance = FinalTermPaper.objects.get(teacher=request.user, subject_name=subject)
            # sessionalmarks_instance = SessionalMarks.objects.get(teacher=request.user, subject_name=subject)
            # recommendations_instance = RecommendationsAndSuggestions.objects.get(teacher=request.user, subject_name=subject)

            # Create forms with existing instances
            # courseobjective_form = CourseObjectiveForm(request.POST, request.FILES, instance=courseobjective_instance)
            # courseoutline_form = CourseOutlineForm(request.POST, request.FILES, instance=courseoutline_instance)
            # weeklyplan_form = WeeklyPlanForm(request.POST, request.FILES, instance=weeklyplan_instance)
            # timetable_form = TimetableForm(request.POST, request.FILES, instance=timetable_instance)
            # attendancerecord_form = AttendanceRecordForm(request.POST, request.FILES, instance=attendancerecord_instance)
            # makeupclass_form = MakeupClassForm(request.POST, request.FILES, instance=makeupclass_instance)
            # counseling_form = CounselingHoursForm(request.POST, request.FILES, instance=counseling_instance)
            # lecturenotes_form = LectureNotesForm(request.POST, request.FILES, instance=lecturenotes_instance)
            # referencematerial_form = ReferenceMaterialForm(request.POST, request.FILES, instance=referencematerial_instance)
            # midterm_form = MidTermPaperForm(request.POST, request.FILES, instance=midterm_instance)
            # finalterm_form = FinalTermPaperForm(request.POST, request.FILES, instance=finalterm_instance)
            # sessionalmarks_form = SessionalMarksForm(request.POST, request.FILES, instance=sessionalmarks_instance)
            # recommendations_form = RecommendationsAndSuggestionsForm(request.POST, request.FILES, instance=recommendations_instance)

            # if semester_type and year:
            #             academicschedule= AcademicSchedule.objects.get(
            #                 teacher=request.user,
            #                 year=Year.objects.get(name=year),
            #                 semester_type=SemesterType.objects.get(name=semester_type),
            #                 subject_name=subject_instance
            #             )
            #             teacher_document.academic_schedule = academicschedule
            
        # Dynamically build the update dict
            # update_data = {}
            # if outline is not None:
            #     update_data['outline_text'] = outline
            # if outlinefile is not None:
            #     update_data['outlinefile'] = outlinefile

            # # Only update if there is something to update
            # if update_data:
            #     CourseOutline.objects.filter(teacher=request.user, subject_name=subject_instance).update(**update_data)

            # AcademicSchedule
            academicschedule, _ = AcademicSchedule.objects.get_or_create(
                teacher=request.user,
                subject_name=subject_instance
            )
            if semester_type:
                academicschedule.semester_type = SemesterType.objects.get(name=semester_type)
            if year:
                academicschedule.year = Year.objects.get(name=year)
            academicschedule.save()

            # CourseOutline
            course_outline, _ = CourseOutline.objects.get_or_create(
                teacher=request.user,
                subject_name=subject_instance
            )
            if outline:
                course_outline.outline_text = outline
            if outlinefile:
                course_outline.outlinefile = outlinefile
            course_outline.save()

            # CourseObjective
            course_objective, _ = CourseObjective.objects.get_or_create(
                teacher=request.user,
                subject_name=subject_instance
            )
            if objective:
                course_objective.objectives = objective
            if objectivefile:
                course_objective.objectivefile = objectivefile
            course_objective.save()

            # WeeklyPlan
            weekly_plan, _ = WeeklyPlan.objects.get_or_create(
                teacher=request.user,
                subject_name=subject_instance
            )
            if weeklyplantopic:
                weekly_plan.weeklyplantopic = weeklyplantopic
            if weeklyplanfile:
                weekly_plan.weeklyplanfile = weeklyplanfile
            weekly_plan.save()

            # Timetable
            timetable, _ = Timetable.objects.get_or_create(
                teacher=request.user,
                subject_name=subject_instance
            )
            if timetablefile:
                timetable.timetablefile = timetablefile
            timetable.save()

            # AttendanceRecord
            attendance_record, _ = AttendanceRecord.objects.get_or_create(
                teacher=request.user,
                subject_name=subject_instance
            )
            if attendance_record_file:
                attendance_record.attendancerecordfile = attendance_record_file
            attendance_record.save()

            # MakeupClass
            makeup_class, _ = MakeupClass.objects.get_or_create(
                teacher=request.user,
                subject_name=subject_instance
            )
            if makeupclasstopic:
                makeup_class.makeupclasstopic = makeupclasstopic
            if makeupclassfile:
                makeup_class.makeupclassfile = makeupclassfile
            makeup_class.save()

            # CounselingHours
            counseling_hours, _ = CounselingHours.objects.get_or_create(
                teacher=request.user,
                subject_name=subject_instance
            )
            if counselinghourstopic:
                counseling_hours.counselinghourtopic = counselinghourstopic
            if counselinghoursfile:
                counseling_hours.counselinghourfile = counselinghoursfile
            counseling_hours.save()

            # LectureNotes
            lecture_notes, _ = LectureNotes.objects.get_or_create(
                teacher=request.user,
                subject_name=subject_instance
            )
            if lecturenotestopic:
                lecture_notes.lecturenotes = lecturenotestopic
            if lecturenotesfile:
                lecture_notes.lecturenotesfile = lecturenotesfile
            lecture_notes.save()

            # ReferenceMaterial
            reference_material, _ = ReferenceMaterial.objects.get_or_create(
                teacher=request.user,
                subject_name=subject_instance
            )
            if referencematerialtopic:
                reference_material.reference_text = referencematerialtopic
            if referencematerialfile:
                reference_material.referencefile = referencematerialfile
            reference_material.save()

            # MidTermPaper
            mid_term_paper, _ = MidTermPaper.objects.get_or_create(
                teacher=request.user,
                subject_name=subject_instance
            )
            if midPaperFile:
                mid_term_paper.mid_paper_file = midPaperFile
            if midSolutionFile:
                mid_term_paper.mid_solution_file = midSolutionFile
            mid_term_paper.save()

            # FinalTermPaper
            final_term_paper, _ = FinalTermPaper.objects.get_or_create(
                teacher=request.user,
                subject_name=subject_instance
            )
            if finalPaperFile:
                final_term_paper.final_paper_file = finalPaperFile
                
            if finalSolutionFile:
                final_term_paper.final_solution_file = finalSolutionFile
            final_term_paper.save()

            # SessionalMarks
            sessional_marks, _ = SessionalMarks.objects.get_or_create(
                teacher=request.user,
                subject_name=subject_instance
            )
            if sessionalMarksFile :
                sessional_marks.sessional_marks_file = sessionalMarksFile
            sessional_marks.save()

            # RecommendationsAndSuggestions
            recommendations_and_suggestions, _ = RecommendationsAndSuggestions.objects.get_or_create(
                teacher=request.user,
                subject_name=subject_instance
            )
            if recommendations:
                recommendations_and_suggestions.recommendations = recommendations
            if recommendationsfile:
                recommendations_and_suggestions.recommendationsandsuggestionsfile = recommendationsfile
            recommendations_and_suggestions.save()
            # Update or create MidTermPaper
            if midPaperFile:
                midpaperfile, _ = MidTermPaper.objects.update_or_create(
                    teacher=request.user,
                    subject_name=subject_instance,
                    defaults={'mid_paper_file': midPaperFile}
                )

                if midtermpapersolutiondata:
                    if isinstance(midtermpapersolutiondata, str):
                        solutions = json.loads(midtermpapersolutiondata)
                    else:
                        solutions = midtermpapersolutiondata

                    for index, item in enumerate(solutions, start=1):
                        MidTermSolution.objects.update_or_create(
                            teacher=request.user,
                            subject_name=subject_instance,
                            mid_term_paper=midpaperfile,
                            solution_number=index,
                            defaults={
                                'category': item.get('category', 'Average'),
                                'marks_obtained': int(item.get('marks', 0)),
                                'solution_file': item.get('file'),
                                'comments': item.get('comments', '')
                            }
                        )

            # Update or create FinalTermPaper
            if finalPaperFile:
                finaltermform, _ = FinalTermPaper.objects.update_or_create(
                    teacher=request.user,
                    subject_name=subject_instance,
                    defaults={'final_paper_file': finalPaperFile}
                )

                if final_term_data:
                    if isinstance(final_term_data, str):
                        solutions = json.loads(final_term_data)
                    else:
                        solutions = final_term_data

                    for index, item in enumerate(solutions, start=1):
                        FinalTermSolution.objects.update_or_create(
                            teacher=request.user,
                            subject_name=subject_instance,
                            final_term_paper=finaltermform,
                            solution_number=index,
                            defaults={
                                'category': item.get('category', 'Average'),
                                'marks_obtained': int(item.get('marks', 0)),
                                'solution_file': item.get('file'),
                                'comments': item.get('comments', '')
                            }
                        )

            for i in range(1, 5):
                    assignment_data = request.POST.get(f'assignment{i}')
                    print(f'Assignment {i} data: {assignment_data}')
                    
                    if assignment_data and assignment_data != '[]':
                        try:
                            assignment_list = json.loads(assignment_data)
                            for item in assignment_list:
                                # Handle file upload
                                file_key = f'assignment{i}file'

                                    
                                # Fix: Access the category directly from item
                                assignment_obj = Assignment.objects.create(
                                    teacher=request.user,
                                    subject_name=subject_instance,
                                    assignment_number=i,
                                    category=item['category'],  # Changed from item.get('assignment{i}Category')
                                    file=file_key,  # Changed from item.get('assignment{i}file')
                                    marks_obtained=item['marks'],  # Changed from item.get('assignment{i}Marks')
                                    comments=item['comments']  # Changed from item.get('assignment{i}Comments')
                                )
                                teacher_document.assignments.add(assignment_obj)
                                print(f"Created assignment: {assignment_obj}")
                        except json.JSONDecodeError as e:
                            print(f'Error decoding JSON for assignment{i}: {str(e)}')
                        except KeyError as e:
                            print(f'Missing key in assignment data: {str(e)}')
                    else:
                        print(f'No assignment{i} data found or empty')
                
                # Process quizzes (similar logic)
            for i in range(1, 5):
                    quiz_data = request.POST.get(f'quiz{i}')
                    print(f'Quiz {i} data: {quiz_data}')
                    
                    if quiz_data and quiz_data != '[]':
                        try:
                            quiz_list = json.loads(quiz_data)

                             
                            for item in quiz_list:
                                    
                                file = item[f'quiz{i}file']
                                fs = FileSystemStorage()
                                filename = fs.save(file.name, file)
                                file_path = fs.url(filename)
                                print(f'File path for assignment {i}: {file_path}')
                                        
                                # Handle file upload
                                # Fix: Access fields directly from item dictionary
                                quiz_obj = Quiz.objects.create(
                                    teacher=request.user,
                                    subject_name=subject_instance,
                                    quiz_number=i,
                                    category=item[f'quiz{i}Category'],  # Changed from item.get('quiz{i}Category')
                                    file=file_path,  # Changed from item.get('quiz{i}file')
                                    marks_obtained=item[f'quiz{i}Marks'],  # Changed from item.get('quiz{i}Marks')
                                    comments=item[f'quiz{i}Comments']  # Changed from item.get('quiz{i}Comments')
                                )
                                
                                teacher_document.quizzes.add(quiz_obj)
                                print(f"Created quiz: {quiz_obj}")
                        except json.JSONDecodeError as e:
                            print(f'Error decoding JSON for quiz{i}: {str(e)}')
                        except KeyError as e:
                            print(f'Missing key in quiz data: {str(e)}')
                    else:
                        print(f'No quiz{i} data found or empty')

               
            teacher_document.status = 'pending'
            teacher_document.save()


            return JsonResponse({"success": True, "message": "Form submitted successfully!"})

    except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    else:    
    
    
                
                # Fetch instances and initialize forms
                academicschedule = AcademicSchedule.objects.get(subject_name=subject_instance, teacher=request.user)
                print(academicschedule)
                academicscheduleform = AcademicScheduleForm(instance=academicschedule)

                # Assuming each model follows the pattern: Model.objects.get(subject_name=subject_instance, teacher=request.user)
                # Replace each 'Model' with the actual model class for each form
                try:
                    course_objective = CourseObjective.objects.get(subject_name=subject_instance, teacher=request.user)
                    course_objective_form = CourseObjectiveForm(instance=course_objective)
                except CourseObjective.DoesNotExist:
                    course_objective_form = CourseObjectiveForm()

                try:
                    course_outline = CourseOutline.objects.get(subject_name=subject_instance, teacher=request.user)
                    course_outline_form = CourseOutlineForm(instance=course_outline)
                except CourseOutline.DoesNotExist:
                    course_outline_form = CourseOutlineForm()
                try:
                # Repeat the same pattern for all other forms
                   weekly_plan = WeeklyPlan.objects.get(subject_name=subject_instance, teacher=request.user)
                   weekly_plan_form = WeeklyPlanForm(instance=weekly_plan)
                except WeeklyPlan.DoesNotExist:
                    weekly_plan_form = WeeklyPlanForm()
                
                try:
                    timetable = Timetable.objects.get(subject_name=subject_instance, teacher=request.user)
                    timetable_form = TimetableForm(instance=timetable)
                except Timetable.DoesNotExist:
                    timetable_form = TimetableForm()
                try:

                   attendance_record = AttendanceRecord.objects.get(subject_name=subject_instance, teacher=request.user)
                   attendance_record_form = AttendanceRecordForm(instance=attendance_record)
                except AttendanceRecord.DoesNotExist:
                    attendance_record_form = AttendanceRecordForm()
                try:
                    
                    makeup_class = MakeupClass.objects.get(subject_name=subject_instance, teacher=request.user)
                    makeup_class_form = MakeupClassForm(instance=makeup_class)
                except MakeupClass.DoesNotExist:
                    makeup_class_form = MakeupClassForm()
                try:
                  counseling_hours = CounselingHours.objects.get(subject_name=subject_instance, teacher=request.user)
                  counseling_hours_form = CounselingHoursForm(instance=counseling_hours)
                except CounselingHours.DoesNotExist:
                    counseling_hours_form = CounselingHoursForm()
                try:
                   lecture_notes = LectureNotes.objects.get(subject_name=subject_instance, teacher=request.user)
                   lecture_notes_form = LectureNotesForm(instance=lecture_notes)
                except LectureNotes.DoesNotExist:
                    lecture_notes_form = LectureNotesForm()
                try:
                   reference_material = ReferenceMaterial.objects.get(subject_name=subject_instance, teacher=request.user)
                   reference_material_form = ReferenceMaterialForm(instance=reference_material)
                except ReferenceMaterial.DoesNotExist:
                    reference_material_form = ReferenceMaterialForm()

                # assignment = Assignment.objects.get(subject_name=subject_instance, teacher=request.user)
                # assignment_form = AssignmentForm(instance=assignment)

                # quiz = Quiz.objects.get(subject_name=subject_instance, teacher=request.user)
                # quiz_form = QuizForm(instance=quiz)

                presentation = Presentation.objects.filter(subject_name=subject_instance, teacher=request.user)
                print(presentation)
                try:
                  mid_term_paper = MidTermPaper.objects.get(subject_name=subject_instance, teacher=request.user)
                  mid_term_paper_form = MidTermPaperForm(instance=mid_term_paper)
                except MidTermPaper.DoesNotExist:
                    mid_term_paper_form = MidTermPaperForm()

                try:

                  final_term_paper = FinalTermPaper.objects.get(subject_name=subject_instance, teacher=request.user)
                  final_term_paper_form = FinalTermPaperForm(instance=final_term_paper)
                except FinalTermPaper.DoesNotExist:
                    final_term_paper_form = FinalTermPaperForm()
                try:


                   sessional_marks = SessionalMarks.objects.get(subject_name=subject_instance, teacher=request.user)
                   sessional_marks_form = SessionalMarksForm(instance=sessional_marks)
                except SessionalMarks.DoesNotExist:
                    sessional_marks_form = SessionalMarksForm()

                try:
                  recommendations_suggestions = RecommendationsAndSuggestions.objects.get(subject_name=subject_instance, teacher=request.user)
                  recommendations_suggestions_form = RecommendationsAndSuggestionsForm(instance=recommendations_suggestions)
                except RecommendationsAndSuggestions.DoesNotExist:
                    recommendations_suggestions_form = RecommendationsAndSuggestionsForm()

                forms = {
                    'academicscheduleform': academicscheduleform,
                    'course_objective_form': course_objective_form,
                    'course_outline_form': course_outline_form,
                    'weekly_plan_form': weekly_plan_form,
                    'timetable_form': timetable_form,
                    'attendance_record_form': attendance_record_form,
                    'makeup_class_form': makeup_class_form,
                    'counseling_hours_form': counseling_hours_form,
                    'lecture_notes_form': lecture_notes_form,
                    'reference_material_form': reference_material_form,
                    'assignment_form': 'assignment_form',
                    'quiz_form': 'quiz_form',
                    'mid_term_paper_form': mid_term_paper_form,
                    'final_term_paper_form': final_term_paper_form,
                    'sessional_marks_form': sessional_marks_form,
                    'recommendations_suggestions_form': recommendations_suggestions_form,
                }
                subject = get_object_or_404(Subject, name=subject)

                schedule = AcademicSchedule.objects.get(teacher=request.user, subject_name=subject)
                selected_semester = schedule.semester_type if schedule else None
                selected_year = schedule.year if schedule else None


                context={
                    'forms':forms,
                    'semester_type': SemesterType.objects.all(),
                    'Year': Year.objects.all(),
    'selected_semester': selected_semester,
    'selected_year': selected_year,

                    'presentation': presentation,
                    'assigment1':Assignment.objects.filter(teacher=request.user, subject_name=subject_instance, assignment_number=1),
                    'assigment2':Assignment.objects.filter(teacher=request.user, subject_name=subject_instance, assignment_number=2),
                    'assigment3':Assignment.objects.filter(teacher=request.user, subject_name=subject_instance, assignment_number=3),
                    'assigment4':Assignment.objects.filter(teacher=request.user, subject_name=subject_instance, assignment_number=4),
                    'quiz1':Quiz.objects.filter(teacher=request.user, subject_name=subject_instance, quiz_number=1),
                    'quiz2':Quiz.objects.filter(teacher=request.user, subject_name=subject_instance, quiz_number=2),
                    'quiz3':Quiz.objects.filter(teacher=request.user, subject_name=subject_instance, quiz_number=3),
                    'quiz4':Quiz.objects.filter(teacher=request.user, subject_name=subject_instance, quiz_number=4),
                

                }

                return render(request, 'edit_upload_folder.html',context)

from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa  # or use WeasyPrint, etc.
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import *
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa

def generate_combined_pdf(request, subject):
    subject_obj = Subject.objects.get(name=subject)
    course_outline= CourseOutline.objects.filter(subject_name=subject_obj, teacher=request.user)
    print(course_outline)

    

    context = {
        'subject': subject_obj,
        'academicschedule': AcademicSchedule.objects.filter(subject_name=subject_obj, teacher=request.user),
        'course_outline': CourseOutline.objects.filter(subject_name=subject_obj, teacher=request.user),
        'course_objective': CourseObjective.objects.filter(subject_name=subject_obj, teacher=request.user),
        'weekly_plan': WeeklyPlan.objects.filter(subject_name=subject_obj, teacher=request.user),
        'timetable': Timetable.objects.filter(subject_name=subject_obj, teacher=request.user),
        'attendance_record': AttendanceRecord.objects.filter(subject_name=subject_obj, teacher=request.user),
        'counseling_hours': CounselingHours.objects.filter(subject_name=subject_obj, teacher=request.user),
        'makeup_class': MakeupClass.objects.filter(subject_name=subject_obj, teacher=request.user),
        'lecture_notes': LectureNotes.objects.filter(subject_name=subject_obj, teacher=request.user),
        'reference_material': ReferenceMaterial.objects.filter(subject_name=subject_obj, teacher=request.user),
        'assignment': Assignment.objects.filter(subject_name=subject_obj, teacher=request.user),
        'quiz': Quiz.objects.filter(subject_name=subject_obj, teacher=request.user),
        'presentation': Presentation.objects.filter(subject_name=subject_obj, teacher=request.user),
        'midterm_paper': MidTermPaper.objects.filter(subject_name=subject_obj, teacher=request.user),
        'finalterm_paper': FinalTermPaper.objects.filter(subject_name=subject_obj, teacher=request.user),
        'sessional_marks': SessionalMarks.objects.filter(subject_name=subject_obj, teacher=request.user),
        'recommendations': RecommendationsAndSuggestions.objects.filter(subject_name=subject_obj, teacher=request.user),
    }

    html = render_to_string('pdf_templates/document_report.html', context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="combined_report.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response

from django.http import FileResponse
from .utils import merge_files_to_pdf  # assuming you put the utility code in utils.py
from django.http import FileResponse
from .utils import create_text_pdf, convert_to_pdf, merge_files_to_pdf
import tempfile

def pdfsview(request, subject):
    subject_instance = Subject.objects.get(name=subject)

    courseoutline = CourseOutline.objects.get(teacher=request.user, subject_name=subject_instance)
    courseobjective = CourseObjective.objects.get(teacher=request.user, subject_name=subject_instance)
    weeklyplan = WeeklyPlan.objects.get(teacher=request.user, subject_name=subject_instance)
    timetable = Timetable.objects.get(teacher=request.user, subject_name=subject_instance)
    attendance_record = AttendanceRecord.objects.get(teacher=request.user, subject_name=subject_instance)
    counselinghours = CounselingHours.objects.get(teacher=request.user, subject_name=subject_instance)
    lecture_notes = LectureNotes.objects.get(teacher=request.user, subject_name=subject_instance)
    reference_material = ReferenceMaterial.objects.get(teacher=request.user, subject_name=subject_instance)
    midterm = MidTermPaper.objects.get(teacher=request.user, subject_name=subject_instance)
    finalterm = FinalTermPaper.objects.get(teacher=request.user, subject_name=subject_instance)
    sessional_marks = SessionalMarks.objects.get(teacher=request.user, subject_name=subject_instance)
    recommendations_suggestions = RecommendationsAndSuggestions.objects.get(teacher=request.user, subject_name=subject_instance)

    # Add text + file in sequence
    files = [
        create_text_pdf(courseoutline.outline_text),
        convert_to_pdf(courseoutline.outlinefile.path),

        create_text_pdf(courseobjective.objectives),
        convert_to_pdf(courseobjective.objectivefile.path),

        create_text_pdf(weeklyplan.weeklyplantopic),
        convert_to_pdf(weeklyplan.weeklyplanfile.path),

        convert_to_pdf(timetable.timetablefile.path),

        convert_to_pdf(attendance_record.attendancerecordfile.path),

        create_text_pdf(counselinghours.counselinghourtopic),
        convert_to_pdf(counselinghours.counselinghourfile.path),

        create_text_pdf(lecture_notes.lecturenotes),
        convert_to_pdf(lecture_notes.lecturenotesfile.path),

        create_text_pdf(reference_material.reference_text),
        convert_to_pdf(reference_material.referencefile.path),

        convert_to_pdf(midterm.mid_paper_file.path),

        convert_to_pdf(finalterm.final_paper_file.path),

        convert_to_pdf(sessional_marks.sessional_marks_file.path),

        create_text_pdf(recommendations_suggestions.recommendations),
        convert_to_pdf(recommendations_suggestions.recommendationsandsuggestionsfile.path),
    ]

    # Merge and return PDF
    output_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    merge_files_to_pdf(files, output_pdf.name)

    return FileResponse(open(output_pdf.name, 'rb'), content_type='application/pdf', filename='merged_course_content.pdf')







from django.core.mail import EmailMessage
from django.http import FileResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .utils import merge_files_to_pdf  # and other imports
import tempfile
import os

@login_required
def pdfemailsendview(request, subject):
    # Check if user has email
    if not request.user.email:
        return HttpResponse("Error: User email is not registered.", status=400)

    try:
        # Your existing model fetching logic
        subject_instance = Subject.objects.get(name=subject)
        courseoutline = CourseOutline.objects.get(teacher=request.user, subject_name=subject_instance)
        courseoutline = CourseOutline.objects.get(teacher=request.user, subject_name=subject_instance)
        courseobjective = CourseObjective.objects.get(teacher=request.user, subject_name=subject_instance)
        weeklyplan = WeeklyPlan.objects.get(teacher=request.user, subject_name=subject_instance)
        timetable = Timetable.objects.get(teacher=request.user, subject_name=subject_instance)
        attendance_record = AttendanceRecord.objects.get(teacher=request.user, subject_name=subject_instance)
        counselinghours = CounselingHours.objects.get(teacher=request.user, subject_name=subject_instance)
        lecture_notes = LectureNotes.objects.get(teacher=request.user, subject_name=subject_instance)
        reference_material = ReferenceMaterial.objects.get(teacher=request.user, subject_name=subject_instance)
        midterm = MidTermPaper.objects.get(teacher=request.user, subject_name=subject_instance)
        finalterm = FinalTermPaper.objects.get(teacher=request.user, subject_name=subject_instance)
        sessional_marks = SessionalMarks.objects.get(teacher=request.user, subject_name=subject_instance)
        recommendations_suggestions = RecommendationsAndSuggestions.objects.get(teacher=request.user, subject_name=subject_instance)


        # File generation logic
        files = [
            create_text_pdf(courseoutline.outline_text),
            convert_to_pdf(courseoutline.outlinefile.path),
            
        create_text_pdf(courseobjective.objectives),
        convert_to_pdf(courseobjective.objectivefile.path),

        create_text_pdf(weeklyplan.weeklyplantopic),
        convert_to_pdf(weeklyplan.weeklyplanfile.path),

        convert_to_pdf(timetable.timetablefile.path),

        convert_to_pdf(attendance_record.attendancerecordfile.path),

        create_text_pdf(counselinghours.counselinghourtopic),
        convert_to_pdf(counselinghours.counselinghourfile.path),

        create_text_pdf(lecture_notes.lecturenotes),
        convert_to_pdf(lecture_notes.lecturenotesfile.path),

        create_text_pdf(reference_material.reference_text),
        convert_to_pdf(reference_material.referencefile.path),

        convert_to_pdf(midterm.mid_paper_file.path),

        convert_to_pdf(finalterm.final_paper_file.path),

        convert_to_pdf(sessional_marks.sessional_marks_file.path),

        create_text_pdf(recommendations_suggestions.recommendations),
        convert_to_pdf(recommendations_suggestions.recommendationsandsuggestionsfile.path),
            # ... rest of your files list ...
        ]

        # Generate merged PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as output_pdf:
            merge_files_to_pdf(files, output_pdf.name)
            
            # Read the generated PDF content
            with open(output_pdf.name, 'rb') as f:
                pdf_content = f.read()

        # Clean up temporary file
        os.unlink(output_pdf.name)

        # Send email with PDF
        email = EmailMessage(
            f'Course Materials for {subject}',
            'Attached is your requested course materials PDF.',
            'syedawaisalishah46@gmail.com',  # Set this in settings.py
            [request.user.email]
        )
        email.attach(f'{subject}_materials.pdf', pdf_content, 'application/pdf')
        email.send(fail_silently=False)

        # Return PDF preview
        return HttpResponse(pdf_content, 
                          content_type='application/pdf',
                          headers={'Content-Disposition': 'inline; filename="course_preview.pdf"'})

    except Subject.DoesNotExist:
        return HttpResponse("Error: Subject not found.", status=404)
    except Exception as e:
        # Handle other exceptions (e.g., model DoesNotExist, email errors)
        return HttpResponse(f"Error: {str(e)}", status=500)
    
@login_required
def pdfsview(request, subject):
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
        midterm = MidTermPaper.objects.get(teacher=request.user, subject_name=subject_instance)
        finalterm = FinalTermPaper.objects.get(teacher=request.user, subject_name=subject_instance)
        sessional_marks = SessionalMarks.objects.get(teacher=request.user, subject_name=subject_instance)
        recommendations_suggestions = RecommendationsAndSuggestions.objects.get(teacher=request.user, subject_name=subject_instance)

        files = []

        def add_text_or_file(text, file_field):
            if text:
                files.append(create_text_pdf(text))
            elif file_field and hasattr(file_field, 'path'):
                files.append(convert_to_pdf(file_field.path))
            # else skip

        # Add each section conditionally
        add_text_or_file(courseoutline.outline_text, courseoutline.outlinefile)
        add_text_or_file(courseobjective.objectives, courseobjective.objectivefile)
        add_text_or_file(weeklyplan.weeklyplantopic, weeklyplan.weeklyplanfile)
        add_text_or_file(None, timetable.timetablefile)
        add_text_or_file(None, attendance_record.attendancerecordfile)
        add_text_or_file(counselinghours.counselinghourtopic, counselinghours.counselinghourfile)
        add_text_or_file(lecture_notes.lecturenotes, lecture_notes.lecturenotesfile)
        add_text_or_file(reference_material.reference_text, reference_material.referencefile)
        add_text_or_file(None, midterm.mid_paper_file)
        add_text_or_file(None, finalterm.final_paper_file)
        add_text_or_file(None, sessional_marks.sessional_marks_file)
        add_text_or_file(recommendations_suggestions.recommendations, recommendations_suggestions.recommendationsandsuggestionsfile)

        if not files:
            return HttpResponse("No data available to generate PDF.", status=204)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as output_pdf:
            merge_files_to_pdf(files, output_pdf.name)
            with open(output_pdf.name, 'rb') as f:
                pdf_content = f.read()
        os.unlink(output_pdf.name)

        response = HttpResponse(pdf_content, content_type='application/pdf')
        filename = f"{subject.replace(' ', '_')}_course_materials.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    except Subject.DoesNotExist:
        return HttpResponse("Error: Subject not found.", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from .models import Message

@login_required
def chat_view(request):
    if request.user.is_superuser:
        users = User.objects.exclude(id=request.user.id)
        messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    
        # Mark all messages as read
        messages.update(is_read=True)

        # Reset unread count
        try:
            profile = TeacherProfile.objects.get(user=request.user)
            profile.unread_message_count = 0
            profile.save()
        except TeacherProfile.DoesNotExist:
            pass


          # Admin can choose any user
    else:
        messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
        
        # Mark all messages as read
        messages.update(is_read=True)

        # Reset unread count
        try:
            profile = TeacherProfile.objects.get(user=request.user)
            profile.unread_message_count = 0
            profile.save()
        except TeacherProfile.DoesNotExist:
            pass


        # Regular user chats only with admin (first superuser)
        admin_user = User.objects.filter(is_superuser=True).first()
        
        users = [admin_user]
    return render(request, 'chats.html', {'users': users})

@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST['receiver_id']
        content = request.POST['content']
        receiver = User.objects.get(id=receiver_id)
        msg = Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return JsonResponse({'status': 'Message sent'})
    return JsonResponse({'status': 'Invalid request'})

@login_required
def get_messages(request):
    other_user_id = request.GET['receiver_id']
    other_user = User.objects.get(id=other_user_id)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')
    data = [{'sender': m.sender.username, 'content': m.content, 'timestamp': m.timestamp.strftime('%H:%M')} for m in messages]
    return JsonResponse({'messages': data})


from django.shortcuts import render
from django.db.models import Count, Max
from .models import TeacherDocument, TeacherProfile
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from django.shortcuts import render
from django.db.models import Count, Max, F, Q
from .models import TeacherDocument, TeacherProfile, AcademicSchedule, Subject
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from django.db import models



from django.shortcuts import render, redirect
from django.db.models import Count, Max, F, Q
from .models import TeacherDocument, TeacherProfile, AcademicSchedule, Subject
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from django.db import models

def admin_dashboard(request):
    profile, created = TeacherProfile.objects.get_or_create(user=request.user)

    if not request.user.is_superuser:
        return redirect('dashboard')
    
    # Overall counts
    total_courses = TeacherDocument.objects.count()
    total_assign = TeacherDocument.objects.filter(status='assign').count()
    total_pending = TeacherDocument.objects.filter(status='pending').count()
    total_approved = TeacherDocument.objects.filter(status='approved').count()
    total_rejected = TeacherDocument.objects.filter(status='rejected').count()
    
    # Get all teachers with their document counts
    teachers = []
    profiles = TeacherProfile.objects.select_related('user').all()
    
    for profile in profiles:
        documents = TeacherDocument.objects.filter(user=profile.user)
        total = documents.count()
        
        if total > 0:
            assign_percent = (documents.filter(status='assign').count() / total) * 100
            pending_percent = (documents.filter(status='pending').count() / total) * 100
            approved_percent = (documents.filter(status='approved').count() / total) * 100
            rejected_percent = (documents.filter(status='rejected').count() / total) * 100
        else:
            assign_percent = pending_percent = approved_percent = rejected_percent = 0
        
        teachers.append({
            'user': profile.user,
            'profile_picture': profile.profile_picture,
            'department_from': profile.department_from,
            'total_courses': total,
            'assign_percent': assign_percent,
            'pending_percent': pending_percent,
            'approved_percent': approved_percent,
            'rejected_percent': rejected_percent
        })
    
    # Semester breakdown
    semester_data = defaultdict(lambda: {
        'total': 0, 
        'pending': 0, 
        'approved': 0, 
        'rejected': 0
    })
    
    # Get academic schedules with their documents
    academic_schedules = AcademicSchedule.objects.prefetch_related(
        'subject_name__teacherdocument_set'
    ).annotate(
        semester_name=F('semester_type__name'),
        year_name=F('year__name')
    )
    
    for schedule in academic_schedules:
        semester = schedule.semester_name or 'Unknown'
        documents = schedule.subject_name.teacherdocument_set.all()
        
        semester_data[semester]['total'] += documents.count()
        semester_data[semester]['pending'] += documents.filter(status='pending').count()
        semester_data[semester]['approved'] += documents.filter(status='approved').count()
        semester_data[semester]['rejected'] += documents.filter(status='rejected').count()
    
    # Year breakdown
    year_data = defaultdict(lambda: {
        'total': 0, 
        'pending': 0, 
        'approved': 0, 
        'rejected': 0
    })
    
    for schedule in academic_schedules:
        year = schedule.year_name or 'Unknown'
        documents = schedule.subject_name.teacherdocument_set.all()
        
        year_data[year]['total'] += documents.count()
        year_data[year]['pending'] += documents.filter(status='pending').count()
        year_data[year]['approved'] += documents.filter(status='approved').count()
        year_data[year]['rejected'] += documents.filter(status='rejected').count()
    
    # Top subjects
    top_subjects = Subject.objects.annotate(
        document_count=Count('teacherdocument'),
        most_common_status=Max('teacherdocument__status')
    ).order_by('-document_count')[:5]
    
    # Status trend data (last 6 months)
    trend_labels = []
    trend_assigned = []
    trend_pending = []
    trend_approved = []
    
    # FIX: Use academic_schedule__created_at instead of created_at
    for i in range(6):
        month = timezone.now() - timedelta(days=30*i)
        month_label = month.strftime("%b %Y")
        trend_labels.append(month_label)
        
        month_start = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # Use academic_schedule__created_at for filtering
        trend_assigned.append(TeacherDocument.objects.filter(
            academic_schedule__created_at__range=[month_start, month_end],
            status='assign'
        ).count())
        
        trend_pending.append(TeacherDocument.objects.filter(
            academic_schedule__created_at__range=[month_start, month_end],
            status='pending'
        ).count())
        
        trend_approved.append(TeacherDocument.objects.filter(
            academic_schedule__created_at__range=[month_start, month_end],
            status='approved'
        ).count())
    
    # Reverse to show oldest first
    trend_labels.reverse()
    trend_assigned.reverse()
    trend_pending.reverse()
    trend_approved.reverse()
    
    # Prepare data for charts
    semester_labels = list(semester_data.keys())
    semester_totals = [d['total'] for d in semester_data.values()]
    
    year_labels = list(year_data.keys())
    year_totals = [d['total'] for d in year_data.values()]
    
    subject_labels = [s.name for s in top_subjects]
    subject_counts = [s.document_count for s in top_subjects]
    
    context = {
        'total_courses': total_courses,
        'total_assign': total_assign,
        'total_pending': total_pending,
        'total_approved': total_approved,
        'total_rejected': total_rejected,
        'teachers': teachers,
        'semester_data': dict(semester_data),
        'year_data': dict(year_data),
        'top_subjects': top_subjects,
        'trend_labels': trend_labels,
        'trend_assigned': trend_assigned,
        'trend_pending': trend_pending,
        'trend_approved': trend_approved,
        'semester_labels': semester_labels,
        'semester_totals': semester_totals,
        'year_labels': year_labels,
        'year_totals': year_totals,
        'subject_labels': subject_labels,
        'subject_counts': subject_counts,
        'profile':profile,
    }
    
    return render(request, 'admin_dashboard.html', context)




from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import AcademicSchedule, SemesterType, TeacherDocument

def admin_create_user(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create teacher profile for the new user
            TeacherProfile.objects.create(user=user)
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('admin_users')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'admin_create_user.html', context)

def admin_academic_management(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    
    years = Year.objects.all()
    semesters = SemesterType.objects.all()
    
    if request.method == 'POST':
        # Handle year creation
        if 'create_year' in request.POST:
            year_name = request.POST.get('year_name')
            if year_name:
                Year.objects.create(name=year_name)
                messages.success(request, f'Year "{year_name}" created successfully!')
        
        # Handle semester creation
        elif 'create_semester' in request.POST:
            semester_name = request.POST.get('semester_name')
            if semester_name:
                SemesterType.objects.create(name=semester_name)
                messages.success(request, f'Semester "{semester_name}" created successfully!')
    
    context = {'years': years, 'semesters': semesters}
    return render(request, 'admin_academic_management.html', context)

def admin_document_management(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    
    documents = TeacherDocument.objects.select_related('user', 'academic_schedule').all()
    
    if request.method == 'POST':
        document_id = request.POST.get('document_id')
        new_status = request.POST.get('new_status')
        
        try:
            document = TeacherDocument.objects.get(id=document_id)
            document.status = new_status
            document.save()
            messages.success(request, f'Document status updated to {new_status}!')
        except TeacherDocument.DoesNotExist:
            messages.error(request, 'Document not found!')
    
    context = {'documents': documents}
    return render(request, 'admin_document_management.html', context)

def admin_users_list(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    
    users = User.objects.select_related('teacherprofile').all()
    context = {'users': users}
    return render(request, 'admin_users_list.html', context)




from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Subject, User, TeacherDocument

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_subject_data_view(request):
    # Get all subjects and teachers for the filter dropdowns
    subjects = Subject.objects.all()
    teachers = User.objects.filter(groups__name='Teachers')  # Assuming teachers are in a 'Teachers' group
    
    # Get filter parameters from request
    selected_subject = request.GET.get('subject')
    selected_teacher = request.GET.get('teacher')
    
    # Start with all teacher documents
    teacher_documents = TeacherDocument.objects.all()
    
    # Apply filters if provided
    if selected_subject:
        teacher_documents = teacher_documents.filter(subject_name_id=selected_subject)
    if selected_teacher:
        teacher_documents = teacher_documents.filter(user_id=selected_teacher)
    
    context = {
        'subjects': subjects,
        'teachers': teachers,
        'teacher_documents': teacher_documents,
        'selected_subject': int(selected_subject) if selected_subject else None,
        'selected_teacher': int(selected_teacher) if selected_teacher else None,
    }
    
    return render(request, 'admin_subject_data.html', context)

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse

@require_POST
@login_required
def clear_notifications(request):
    request.user.notifications.filter(is_read=True).delete()
    return JsonResponse({'status': 'deleted'})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import TeacherProfile

@login_required
def get_unread_message_count(request):
    try:
        profile = TeacherProfile.objects.get(user=request.user)
        return JsonResponse({'count': profile.unread_message_count})
    except TeacherProfile.DoesNotExist:
        return JsonResponse({'count': 0})
