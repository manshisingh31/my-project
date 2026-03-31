from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=100)  # course title

    def __str__(self):
        return self.title


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    courses = models.ManyToManyField(Course, blank=True)  # multiple courses

    def __str__(self):
        return self.name