

from django.shortcuts import render, redirect
from .models import Student, Course
from .forms import StudentForm

def dashboard(request):
    return render(request, 'students/dashboard.html')


def users(request):
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'students/users.html', context)


def courses(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Course.objects.get_or_create(title=title)  # prevent duplicates
        return redirect('courses')

    all_courses = Course.objects.all()
    context = {'courses': all_courses}
    return render(request, 'students/courses.html', context)


def enroll(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()  # save() handles ManyToMany relationships automatically
            return redirect('users')
    else:
        form = StudentForm()
    return render(request, 'students/enroll.html', {'form': form})


def records(request):
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'students/users.html', context)  # can reuse users.html