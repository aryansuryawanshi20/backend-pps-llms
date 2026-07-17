from django.urls import path
from .views import StudentList, CourseList, VideoList
from .login_views import student_login
from .views import pending_students
from .views import approve_student
urlpatterns = [

    path("students/", StudentList.as_view()),

    path("courses/", CourseList.as_view()),

    path("videos/", VideoList.as_view()),
    
    path("student-login/",student_login),
    
    path("pending-students/",pending_students),
    path("approve-student/",approve_student),

]