from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('create_course/', views.create_course, name='create_course'),
    path('add_chapter/<int:course_id>/', views.add_chapter, name='add_chapter'),
    path('add_lesson/<int:chapter_id>/', views.add_lesson, name='add_lesson'),
    path('join_course/<int:course_id>/', views.join_course, name='join_course'),
    path('approve_request/<int:enrollment_id>/', views.approve_request, name='approve_request'),
    path('create_course/', views.create_course, name='create_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    
    # Chapter CRUD
    path('add_chapter/<int:course_id>/', views.add_chapter, name='add_chapter'),
    path('view_chapters/<int:course_id>/', views.view_chapters, name='view_chapters'),
    path('delete_chapter/<int:chapter_id>/', views.delete_chapter, name='delete_chapter'),

    # Lesson CRUD
    path('add_lesson/<int:chapter_id>/', views.add_lesson, name='add_lesson'),
    path('update_lesson/<int:lesson_id>/', views.update_lesson, name='update_lesson'),
    path('delete_lesson/<int:lesson_id>/', views.delete_lesson, name='delete_lesson'),
    path('view_lessons/<int:chapter_id>/', views.view_lessons, name='view_lessons'),
    path('view_lesson/<int:lesson_id>/', views.view_lesson, name='view_lesson'),
    
    # add assignment
    path('add_question/<int:lesson_id>/', views.add_question, name='add_question'),
    path('assignment_view/<int:lesson_id>/', views.assignment_view, name='assignment_view'),
   
   

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
