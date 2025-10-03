from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Profile, Course, Chapter, Lesson, CourseEnrollment,Question,Option,Question,Option
from django.http import HttpResponse
# Signup 
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists. Choose another.'})

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already registered.'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Create Profile linked to user
        profile = Profile.objects.create(user=user, role=role)
        profile.save()

        return redirect('/login/')
    return render(request, 'signup.html')

# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.profile.role == "teacher":
                print('hi')
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
    return render(request, 'login.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Teacher Dashboard
def teacher_dashboard(request):
    courses = Course.objects.filter(teacher=request.user) #getting all course created by that login Teacher
    pending_requests = CourseEnrollment.objects.filter(course__teacher=request.user, is_approved=False)
    return render(request, 'teacher_dashboard.html', {'courses': courses, 'pending_requests': pending_requests})

# Student Dashboard 
def student_dashboard(request):
    # taking all the course where student is enrolled and approved
    approved_courses = CourseEnrollment.objects.filter(student=request.user, is_approved=True)
    # taking all course in system
    all_courses = Course.objects.all()
    return render(request, 'student_dashboard.html', {'approved_courses': approved_courses, 'all_courses': all_courses})

# Course CRUD 
def create_course(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        Course.objects.create(teacher=request.user, title=title, description=description)
        return redirect('teacher_dashboard')
    return render(request, 'create_course.html')

# Chapter CRUD 
def add_chapter(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    if request.method == "POST":
        title = request.POST['title']
        Chapter.objects.create(course=course, title=title)
        return redirect('view_chapters', course_id=course.id)
    return render(request, 'add_chapter.html', {'course': course})

def view_chapters(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    chapters = course.chapters.all()
    return render(request, 'view_chapters.html', {'course': course, 'chapters': chapters})

def delete_chapter(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id, course__teacher=request.user)
    course_id = chapter.course.id
    chapter.delete()
    return redirect('view_chapters', course_id=course_id)

# Lesson CRUD 
def add_lesson(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id, course__teacher=request.user)
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        link = request.POST['link']
        Lesson.objects.create(chapter=chapter, title=title, content=content, video=link)
        return redirect('view_lessons', chapter_id=chapter.id)
    return render(request, 'add_lesson.html', {'chapter': chapter})

def view_lessons(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id, course__teacher=request.user)
    lessons = chapter.lessons.all()
    return render(request, 'view_lessons.html', {'chapter': chapter, 'lessons': lessons})

def update_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, chapter__course__teacher=request.user)
    if request.method == "POST":
        lesson.title = request.POST['title']
        lesson.content = request.POST['content']
        lesson.video = request.POST['link']
        
        lesson.save()
        return redirect('view_lessons', chapter_id=lesson.chapter.id)
    return render(request, 'update_lesson.html', {'lesson': lesson})

def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, chapter__course__teacher=request.user)
    chapter_id = lesson.chapter.id
    lesson.delete()
    return redirect('view_lessons', chapter_id=chapter_id)

# Student Join Course 
def join_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    CourseEnrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('student_dashboard')

#  Approve Student 
def approve_request(request, enrollment_id):
    enrollment = get_object_or_404(CourseEnrollment, id=enrollment_id)
    enrollment.is_approved = True
    enrollment.save()
    return redirect('teacher_dashboard')
# blog content
def view_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'data.html', {'lesson': lesson})



def delete_course(request,course_id):
    obj = Course.objects.get(id=course_id)
    print(obj.teacher)
    print(obj.title)
    print(obj.description)
    obj.delete()
    return redirect('teacher_dashboard')
    
    


def add_question(request,lesson_id):
    if request.method == "POST":
        question_text = request.POST.get("text")
        option1 = request.POST.get("option1")
        option2 = request.POST.get("option2")
        option3 = request.POST.get("option3")
        option4 = request.POST.get("option4")
        correct_option = int(request.POST.get("correct_option"))  # 1,2,3,4

        # save question
        lesson = Lesson.objects.get(id=lesson_id)
        question = Question.objects.create(lesson=lesson, text=question_text)

        # save options
        options = [option1, option2, option3, option4]

        for i in range(4):
            Option.objects.create(
                question=question,
                text=options[i],
                is_correct=(i + 1 == correct_option)  # since correct_option is 1,2,3,4
            )


        return redirect("add_question", lesson_id=lesson.id)


    lessons = Lesson.objects.all()
    return render(request, "add_question.html", {"lessons": lessons})




def assignment_view(request, lesson_id):

    if request.method == "POST":
        lesson = get_object_or_404(Lesson, id=lesson_id)
        questions = lesson.questions.prefetch_related("options").all()
        total_score =  0
        your_score = 0
        for q in questions:
            total_score +=1
            question_id = q.id
            selected_option = request.POST.get(f"answer_{q.id}")  
            print(f"Question {q.id} selected option:", selected_option)
            
            obj = Option.objects.get(id=selected_option)
            print(obj.is_correct)
            if obj.is_correct == True:
                your_score+=1
                
        print(total_score)       
        print(your_score)
                

        return render(request,"Student_Score_card.html",{"total_score": total_score,"your_score":your_score})

    else:
        lesson = get_object_or_404(Lesson, id=lesson_id)
        questions = lesson.questions.prefetch_related("options").all()
        return render(request, "assignment.html", {"lesson": lesson, "questions": questions})
