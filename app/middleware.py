from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class CustomMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # Paths that require authentication
        restricted_paths = [
            "/teacher/", "/student/", "/create_course/", "/delete_course/",
            "/add_chapter/", "/view_chapters/", "/delete_chapter/",
            "/add_lesson/", "/update_lesson/", "/delete_lesson/",
            "/view_lessons/", "/view_lesson/", "/add_question/",
            "/assignment_view/", "/join_course/", "/approve_request/"
        ]

        # Student cannot access these
        student_restricted = [
            "/teacher/", "/create_course/", "/delete_course/",
            "/add_chapter/", "/delete_chapter/", "/add_lesson/",
            "/update_lesson/", "/delete_lesson/", "/add_question/"
        ]

        # Teacher cannot access these
        teacher_restricted = [
            "/student/", "/join_course/", "/assignment_view/"
        ]

        # If user is not logged in and tries restricted URLs
        if not request.user.is_authenticated:
            if any(request.path.startswith(path) for path in restricted_paths):
                return redirect(reverse("login"))

        # If user is authenticated
        if request.user.is_authenticated:
            # Superuser → allow everything
            if request.user.is_superuser:
                return None

            # Get user role safely
            role = getattr(getattr(request.user, "profile", None), "role", None)

            # Student restrictions
            if role == "student":
                if any(request.path.startswith(path) for path in student_restricted):
                    return redirect(reverse("student_dashboard"))

            # Teacher restrictions
            if role == "teacher":
                if any(request.path.startswith(path) for path in teacher_restricted):
                    return redirect(reverse("teacher_dashboard"))

        return None  # continue as normal