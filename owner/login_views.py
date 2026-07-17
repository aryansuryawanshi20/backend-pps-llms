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