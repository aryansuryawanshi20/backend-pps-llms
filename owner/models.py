from django.db import models


# ==========================
# Student
# ==========================

class Student(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=20)

    degree = models.CharField(max_length=100)

    semester = models.CharField(max_length=50)

    college = models.CharField(max_length=200)

    # Multiple courses comma separated
    course = models.TextField()

    transaction_id = models.CharField(max_length=100)

    payment_screenshot = models.URLField(blank=True)

    username = models.CharField(max_length=100, blank=True)

    password = models.CharField(max_length=100, blank=True)

    approved = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ==========================
# Course
# ==========================

class Course(models.Model):

    title = models.CharField(max_length=200)

    price = models.IntegerField()

    description = models.TextField()

    thumbnail = models.URLField(blank=True)

    def __str__(self):
        return self.title


# ==========================
# Video
# ==========================

class Video(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    url = models.TextField()

    demo = models.BooleanField(default=False)

    def __str__(self):
        return self.title