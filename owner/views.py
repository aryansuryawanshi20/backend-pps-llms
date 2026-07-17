from rest_framework import generics
from .models import Student, Course, Video
from .serializers import StudentSerializer, CourseSerializer, VideoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from django.core.mail import send_mail

import random
import string


class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class VideoList(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    
@api_view(["GET"])

def pending_students(request):

    students = Student.objects.filter(approved=False)

    serializer = StudentSerializer(students,many=True)

    return Response(serializer.data)   

def generate_password():

    chars = string.ascii_letters + string.digits

    return "".join(

        random.choice(chars)

        for _ in range(8)

    ) 

@api_view(["POST"])

def approve_student(request):

    student = Student.objects.get(

        id=request.data["id"]

    )

    student.username = "PPS" + str(student.id).zfill(4)

    student.password = generate_password()

    student.approved = True

    student.save()
    send_mail(
        "Welcome To ProPython Solutions",
        f"""

    Hello {student.name},

    Congratulations!

    Your account has been approved.

    Username:
    {student.username}

    Password:
    {student.password}

    Login:
    https://propythonsolutions.netlify.app

    Regards,
    ProPython Solutions

    """,
        None,

        [student.email],

       fail_silently=False

    )


    return Response({

        "success":True

    })