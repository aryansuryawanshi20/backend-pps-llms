from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student


TEMP_STUDENTS = [
    {
        "username": "JAVA001",
        "password": "java123",
        "name": "Demo Java Student",
        "email": "java@demo.com",
        "course": ["Java Programming"]
    },
    {
        "username": "C001",
        "password": "c123",
        "name": "Demo C Student",
        "email": "c@demo.com",
        "course": ["C Programming"]
    },
    {
        "username": "DEMO001",
        "password": "demo123",
        "name": "Demo Student",
        "email": "demo@pps.com",
        "course": [
            "Java Programming",
            "C Programming",
            "Prompt Engineering"
        ]
    }
]


@api_view(["POST"])
def student_login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    # ------------------------
    # Temporary Students
    # ------------------------

    for student in TEMP_STUDENTS:

        if (
            student["username"] == username
            and
            student["password"] == password
        ):

            return Response({

                "success": True,
                "name": student["name"],
                "email": student["email"],
                "course": student["course"]

            })

    # ------------------------
    # Database Students
    # ------------------------

    try:

        student = Student.objects.get(

            username=username,
            password=password,
            approved=True

        )

        return Response({

            "success": True,
            "name": student.name,
            "email": student.email,
            "course": student.course.split(",")

        })

    except Student.DoesNotExist:

        return Response({

            "success": False,
            "message": "Invalid Credentials"

        })