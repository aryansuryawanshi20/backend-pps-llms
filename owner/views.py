from rest_framework import generics
from .models import Student, Course, Video
from .serializers import StudentSerializer, CourseSerializer, VideoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from django.core.mail import send_mail
from django.conf import settings
import requests
import json
import os

import random
import string
from django.db.models import Count

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
    print("******** USING BREVO API ********")
    try:
        student = Student.objects.get(id=request.data["id"])

        student.username = "PPS" + str(student.id).zfill(4)
        student.password = generate_password()
        student.approved = True
        student.save()

        headers = {
            "accept": "application/json",
            "api-key": os.getenv("BREVO_API_KEY"),
            "content-type": "application/json",
        }

        payload = {
            "sender": {
                "name": "ProPythonSolutions",
                "email": "propythonsolutions@gmail.com"
            },
            "to": [
                {
                    "email": student.email,
                    "name": student.name
                }
            ],
            "subject": "Welcome To ProPython Solutions",
            "htmlContent": f"""
            <h2>Welcome {student.name}</h2>

            <p>Congratulations! Your account has been approved.</p>

            <h3>Login Details</h3>

            <b>Username:</b> {student.username}<br>
            <b>Password:</b> {student.password}<br><br>

            <a href="https://propythonsolutions.netlify.app/login">
                Login Here
            </a>

            <br><br>

            Regards,<br>
            <b>ProPython Solutions</b>
            """
        }

        response = requests.post(
            
            "https://api.brevo.com/v3/smtp/email",
            headers=headers,
            json=payload
        )

        print("Brevo Status:", response.status_code)
        print("Brevo Response:", response.text)

        if response.status_code not in [200, 201, 202]:
            return Response(
                {
                    "success": False,
                    "error": response.text
                },
                status=500
            )

        return Response(
            {
                "success": True
            }
        )

    except Exception as e:
        import traceback

        print(traceback.format_exc())

        return Response(
            {
                "success": False,
                "error": str(e)
            },
            status=500
        )
@api_view(["GET"])
def dashboard_data(request):

    data = {

        "total_students": Student.objects.count(),

        "approved_students": Student.objects.filter(
            approved=True
        ).count(),

        "pending_students": Student.objects.filter(
            approved=False
        ).count(),

        "total_courses": Course.objects.count(),

        "total_videos": Video.objects.count(),

        "approved_list": StudentSerializer(

            Student.objects.filter(
                approved=True
            ).order_by("-created"),

            many=True

        ).data

    }

    return Response(data)


@api_view(["DELETE"])
def delete_course(request,id):

    try:

        course=Course.objects.get(id=id)

        course.delete()

        return Response({

            "success":True

        })

    except:

        return Response({

            "success":False

        },status=404)        
        