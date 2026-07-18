from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student


@api_view(["POST"])
def student_login(request):

    username=request.data.get("username")

    password=request.data.get("password")

    try:

        student=Student.objects.get(

            username=username,

            password=password,

            approved=True

        )

        return Response({

            "success":True,

            "name":student.name,

            "email":student.email

        })

    except:

        return Response({

            "success":False,

            "message":"Invalid Credentials"

        })
        
TEMP_STUDENTS = [
    {
        "username": "JAVA001",
        "password": "java123",
        "name": "Demo Java Student",
        "course": ["Java Programming"]
    },
    {
        "username": "C001",
        "password": "c123",
        "name": "Demo C Student",
        "course": ["C Programming"]
    },
    {
        "username": "DEMO001",
        "password": "demo123",
        "name": "Demo Student",
        "course": [
            "Java Programming",
            "C Programming",
            "Prompt Engineering"
        ]
    }
]        